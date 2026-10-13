"""Janela principal do Navegador Nimbus em PySide6."""

from typing import Dict, List, Optional
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QProgressBar,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTabBar,
    QVBoxLayout,
    QWidget,
)

from nimbus.core.constants import (
    BrowserConfig,
    DEFAULT_HOME_URL,
    ICON_PATH,
    normalize_input_url,
)
from nimbus.core.tab_manager import TabManager
from nimbus.engine.web_view import NimbusWebView
from nimbus.ui.navigation_bar import NavigationBar
from nimbus.ui.theme import NIMBUS_DARK_THEME_QSS


class NimbusMainWindow(QMainWindow):
    """
    Janela Principal do Navegador Nimbus.
    Equivalente limpo e desacoplado a MainWindow.xaml + MainWindow.xaml.cs.
    """

    def __init__(self, config: Optional[BrowserConfig] = None) -> None:
        super().__init__()
        self._config = config or BrowserConfig()
        self._tab_manager = TabManager()
        self._profile: Optional[QWebEngineProfile] = None
        self._closed_tabs_history: List[str] = []
        self._devtools_views: Dict[str, QWebEngineView] = {}

        self._setup_window()
        self._setup_downloads()
        self._setup_ui()
        self._setup_shortcuts()
        self._setup_initial_tab()

    def _setup_downloads(self) -> None:
        """Configura gerenciador de downloads para Salvar Página e arquivos."""
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self._on_download_requested)

    def _on_download_requested(self, download) -> None:
        """Abre caixa de diálogo para salvar arquivo/página quando solicitado."""
        from PySide6.QtWidgets import QFileDialog
        suggested = download.suggestedFileName() or download.downloadFileName() or "pagina.html"
        save_path, _ = QFileDialog.getSaveFileName(self, "Salvar Como...", suggested)
        if save_path:
            import os
            download.setDownloadDirectory(os.path.dirname(save_path))
            download.setDownloadFileName(os.path.basename(save_path))
            download.accept()
        else:
            download.cancel()

    def _setup_window(self) -> None:
        self.setWindowTitle(self._config.window_title)
        self.resize(self._config.initial_width, self._config.initial_height)
        self.setMinimumSize(self._config.min_width, self._config.min_height)

        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        self.setStyleSheet(NIMBUS_DARK_THEME_QSS)

    def _setup_ui(self) -> None:
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Faixa Superior de Abas (Top Header estilo Chrome)
        tab_header_widget = QWidget()
        tab_header_widget.setObjectName("TabHeaderContainer")
        tab_header_layout = QHBoxLayout(tab_header_widget)
        tab_header_layout.setContentsMargins(8, 6, 8, 0)
        tab_header_layout.setSpacing(4)

        self.tab_bar = QTabBar(self)
        self.tab_bar.setObjectName("NimbusTabBar")
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.setMovable(True)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setDrawBase(False)
        self.tab_bar.currentChanged.connect(self._on_tab_changed)
        self.tab_bar.tabCloseRequested.connect(self._on_close_tab)
        tab_header_layout.addWidget(self.tab_bar)

        # Botão '+' para nova aba integrado ao lado da última aba
        new_tab_btn = QPushButton("+")
        new_tab_btn.setObjectName("NewTabButton")
        new_tab_btn.setToolTip("Nova guia (Ctrl+T)")
        new_tab_btn.clicked.connect(lambda: self.create_new_tab(self._config.default_home_url))
        tab_header_layout.addWidget(new_tab_btn)
        tab_header_layout.addStretch()

        root_layout.addWidget(tab_header_widget)

        # 2. Barra de Navegação (abaixo das abas)
        self.nav_bar = NavigationBar(self)
        self.nav_bar.back_requested.connect(self._on_back)
        self.nav_bar.forward_requested.connect(self._on_forward)
        self.nav_bar.reload_requested.connect(self._on_reload)
        self.nav_bar.home_requested.connect(self._on_home)
        self.nav_bar.url_submitted.connect(self._on_navigate_to_url)
        self.nav_bar.devtools_requested.connect(self._on_toggle_current_devtools)
        self.nav_bar.downloads_requested.connect(self._on_save_page)
        self.nav_bar.menu_requested.connect(self._show_app_menu)
        root_layout.addWidget(self.nav_bar)

        # 3. Barra de Progresso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("ProgressBar")
        self.progress_bar.setFixedHeight(2)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        root_layout.addWidget(self.progress_bar)

        # 4. Container de Conteúdo Web
        self.stack_widget = QStackedWidget(self)
        self.stack_widget.setObjectName("WebContentStack")
        root_layout.addWidget(self.stack_widget)

    def _setup_shortcuts(self) -> None:
        """Configura os atalhos de teclado padrão do Google Chrome."""
        # Ctrl+T: Nova Aba
        QShortcut(QKeySequence("Ctrl+T"), self, activated=lambda: self.create_new_tab(self._config.default_home_url))

        # Ctrl+W / Ctrl+F4: Fechar Aba Atual
        QShortcut(QKeySequence("Ctrl+W"), self, activated=self._close_current_tab)
        QShortcut(QKeySequence("Ctrl+F4"), self, activated=self._close_current_tab)

        # Ctrl+Shift+T: Reabrir Última Aba Fechada
        QShortcut(QKeySequence("Ctrl+Shift+T"), self, activated=self._reopen_last_closed_tab)

        # F12 / Ctrl+Shift+I: Alternar DevTools
        QShortcut(QKeySequence("F12"), self, activated=self._on_toggle_current_devtools)
        QShortcut(QKeySequence("Ctrl+Shift+I"), self, activated=self._on_toggle_current_devtools)

        # Ctrl+S: Salvar Página
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self._on_save_page)

        # Ctrl+R / F5: Recarregar
        QShortcut(QKeySequence("Ctrl+R"), self, activated=self._on_reload)
        QShortcut(QKeySequence("F5"), self, activated=self._on_reload)

        # Ctrl+Shift+R / Ctrl+F5: Hard Reload
        QShortcut(QKeySequence("Ctrl+Shift+R"), self, activated=self._hard_reload)
        QShortcut(QKeySequence("Ctrl+F5"), self, activated=self._hard_reload)

        # Ctrl+L / Alt+D / F6: Focar Barra de Endereço
        QShortcut(QKeySequence("Ctrl+L"), self, activated=self._focus_url_bar)
        QShortcut(QKeySequence("Alt+D"), self, activated=self._focus_url_bar)
        QShortcut(QKeySequence("F6"), self, activated=self._focus_url_bar)

        # Ctrl+Tab / Ctrl+PageDown: Próxima Aba
        QShortcut(QKeySequence("Ctrl+Tab"), self, activated=self._next_tab)
        QShortcut(QKeySequence("Ctrl+PgDown"), self, activated=self._next_tab)

        # Ctrl+Shift+Tab / Ctrl+PageUp: Aba Anterior
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, activated=self._prev_tab)
        QShortcut(QKeySequence("Ctrl+PgUp"), self, activated=self._prev_tab)

        # Alt+Left: Voltar / Alt+Right: Avançar
        QShortcut(QKeySequence("Alt+Left"), self, activated=self._on_back)
        QShortcut(QKeySequence("Alt+Right"), self, activated=self._on_forward)

        # Ctrl+1 a Ctrl+8: Ir para aba específica
        for i in range(1, 9):
            QShortcut(QKeySequence(f"Ctrl+{i}"), self, activated=lambda idx=i-1: self._select_tab_index(idx))

        # Ctrl+9: Ir para a última aba
        QShortcut(QKeySequence("Ctrl+9"), self, activated=self._select_last_tab)

    def _focus_url_bar(self) -> None:
        self.nav_bar.url_input.setFocus()
        self.nav_bar.url_input.selectAll()

    def _close_current_tab(self) -> None:
        idx = self.tab_bar.currentIndex()
        if idx >= 0:
            self._on_close_tab(idx)

    def _reopen_last_closed_tab(self) -> None:
        if self._closed_tabs_history:
            last_url = self._closed_tabs_history.pop()
            self.create_new_tab(last_url)

    def _hard_reload(self) -> None:
        web_view = self.get_current_web_view()
        if web_view:
            web_view.reload()

    def _next_tab(self) -> None:
        total = self.tab_bar.count()
        if total > 1:
            next_idx = (self.tab_bar.currentIndex() + 1) % total
            self.tab_bar.setCurrentIndex(next_idx)

    def _prev_tab(self) -> None:
        total = self.tab_bar.count()
        if total > 1:
            prev_idx = (self.tab_bar.currentIndex() - 1 + total) % total
            self.tab_bar.setCurrentIndex(prev_idx)

    def _select_tab_index(self, index: int) -> None:
        if index < self.tab_bar.count():
            self.tab_bar.setCurrentIndex(index)

    def _select_last_tab(self) -> None:
        total = self.tab_bar.count()
        if total > 0:
            self.tab_bar.setCurrentIndex(total - 1)

    def _setup_initial_tab(self) -> None:
        self.create_new_tab(self._config.default_home_url)

    def create_new_tab(self, url: str) -> NimbusWebView:
        """Cria e anexa uma nova aba de navegação."""
        tab_model = self._tab_manager.add_tab(url=url, title="Nova Aba")
        web_view = NimbusWebView(
            tab_id=tab_model.id,
            profile=self._profile,
            config=self._config,
            parent=self.stack_widget,
        )

        # Conexão de sinais do WebView
        web_view.title_updated.connect(lambda title, w=web_view: self._update_tab_title(w, title))
        web_view.url_updated.connect(lambda qurl, w=web_view: self._update_tab_url(w, qurl))
        web_view.loading_progress.connect(self._update_progress)
        web_view.favicon_updated.connect(lambda icon, w=web_view: self._update_tab_favicon(w, icon))

        # Adiciona aba visual no QTabBar e página no QStackedWidget
        self.stack_widget.addWidget(web_view)
        idx = self.tab_bar.addTab("Nova Aba")

        # Botão fechar customizado ('×') para evitar bugs de rendering de close-button do QSS nativo
        close_btn = QPushButton("×")
        close_btn.setProperty("class", "TabCloseButton")
        close_btn.setToolTip("Fechar guia (Ctrl+W)")
        close_btn.clicked.connect(lambda _, w=web_view: self._close_tab_by_widget(w))
        self.tab_bar.setTabButton(idx, QTabBar.ButtonPosition.RightSide, close_btn)

        self.tab_bar.setCurrentIndex(idx)
        self.stack_widget.setCurrentIndex(idx)

        # Navega para a URL
        target_url = normalize_input_url(url)
        web_view.setUrl(QUrl(target_url))
        return web_view

    def _close_tab_by_widget(self, web_view: NimbusWebView) -> None:
        idx = self.stack_widget.indexOf(web_view)
        if idx != -1:
            self._on_close_tab(idx)

    def get_current_web_view(self) -> Optional[NimbusWebView]:
        """Retorna o WebView da aba ativa no momento."""
        current_widget = self.stack_widget.currentWidget()
        if isinstance(current_widget, NimbusWebView):
            return current_widget
        return None

    def _on_tab_changed(self, index: int) -> None:
        if index < 0 or index >= self.stack_widget.count():
            return
        self.stack_widget.setCurrentIndex(index)
        widget = self.stack_widget.widget(index)
        if isinstance(widget, NimbusWebView):
            self._tab_manager.set_active(widget.tab_id)
            self.nav_bar.set_url(widget.url().toString())
            self.nav_bar.update_navigation_state(
                widget.history().canGoBack(),
                widget.history().canGoForward(),
            )

    def _on_close_tab(self, index: int) -> None:
        widget = self.stack_widget.widget(index)
        if isinstance(widget, NimbusWebView):
            current_url = widget.url().toString()
            if current_url and current_url != "about:blank":
                self._closed_tabs_history.append(current_url)

        if self.tab_bar.count() <= 1:
            # Se for a última aba, fecha a janela
            self.close()
            return

        if isinstance(widget, NimbusWebView):
            self._tab_manager.remove_tab(widget.tab_id)
            self.tab_bar.removeTab(index)
            self.stack_widget.removeWidget(widget)
            if widget.tab_id in self._devtools_views:
                dev = self._devtools_views.pop(widget.tab_id)
                dev.deleteLater()
            widget.dispose()

    def _on_back(self) -> None:
        web_view = self.get_current_web_view()
        if web_view and web_view.history().canGoBack():
            web_view.back()

    def _on_forward(self) -> None:
        web_view = self.get_current_web_view()
        if web_view and web_view.history().canGoForward():
            web_view.forward()

    def _on_reload(self) -> None:
        web_view = self.get_current_web_view()
        if web_view:
            web_view.reload()

    def _on_home(self) -> None:
        web_view = self.get_current_web_view()
        if web_view:
            web_view.setUrl(QUrl(self._config.default_home_url))

    def _on_navigate_to_url(self, raw_url: str) -> None:
        web_view = self.get_current_web_view()
        if web_view:
            normalized = normalize_input_url(raw_url)
            web_view.setUrl(QUrl(normalized))

    def _update_tab_title(self, web_view: NimbusWebView, title: str) -> None:
        idx = self.stack_widget.indexOf(web_view)
        if idx != -1:
            self.tab_bar.setTabText(idx, title)

    def _update_tab_url(self, web_view: NimbusWebView, qurl: QUrl) -> None:
        if web_view == self.get_current_web_view():
            self.nav_bar.set_url(qurl.toString())
            self.nav_bar.update_navigation_state(
                web_view.history().canGoBack(),
                web_view.history().canGoForward(),
            )

    def _update_tab_favicon(self, web_view: NimbusWebView, icon: QIcon) -> None:
        idx = self.stack_widget.indexOf(web_view)
        if idx != -1 and not icon.isNull():
            self.tab_bar.setTabIcon(idx, icon)

    def _update_progress(self, progress: int) -> None:
        if progress < 100:
            self.progress_bar.setValue(progress)
            self.progress_bar.show()
        else:
            self.progress_bar.hide()

    def _on_toggle_current_devtools(self) -> None:
        """Abre ou fecha o DevTools para o WebView atualmente ativo."""
        web_view = self.get_current_web_view()
        if web_view:
            self.toggle_devtools(web_view)

    def toggle_devtools(self, web_view: NimbusWebView) -> None:
        """Abre o DevTools nativo do Chromium em uma janela dedicada ou foca a existente."""
        tab_id = web_view.tab_id
        if tab_id in self._devtools_views and not self._devtools_views[tab_id].isHidden():
            # Se já está aberto, traz para frente
            dev_view = self._devtools_views[tab_id]
            dev_view.raise_()
            dev_view.activateWindow()
            return

        dev_view = QWebEngineView()
        dev_view.setWindowTitle(f"DevTools — {web_view.title() or 'Nimbus'}")
        dev_view.resize(950, 650)
        web_view.page().setDevToolsPage(dev_view.page())
        dev_view.show()
        self._devtools_views[tab_id] = dev_view

    def _on_save_page(self) -> None:
        """Dispara a ação de salvar página do WebView ativo."""
        from PySide6.QtWebEngineCore import QWebEnginePage
        web_view = self.get_current_web_view()
        if web_view:
            web_view.page().triggerAction(QWebEnginePage.WebAction.SavePage)

    def _show_app_menu(self) -> None:
        """Exibe o menu de opções do canto superior direito."""
        menu = QMenu(self)
        menu.setObjectName("NimbusContextMenu")

        act_new_tab = menu.addAction("Nova Guia\tCtrl+T")
        act_new_tab.triggered.connect(lambda: self.create_new_tab(self._config.default_home_url))

        act_reopen = menu.addAction("Reabrir Guia Fechada\tCtrl+Shift+T")
        act_reopen.setEnabled(len(self._closed_tabs_history) > 0)
        act_reopen.triggered.connect(self._reopen_last_closed_tab)

        menu.addSeparator()

        act_save = menu.addAction("Salvar Página Como...\tCtrl+S")
        act_save.triggered.connect(self._on_save_page)

        act_devtools = menu.addAction("Ferramentas do Desenvolvedor\tF12")
        act_devtools.triggered.connect(self._on_toggle_current_devtools)

        menu.addSeparator()

        act_about = menu.addAction("Sobre o Nimbus")
        act_about.triggered.connect(self._show_about_dialog)

        # Posiciona abaixo do botão de menu
        btn_pos = self.nav_bar.menu_button.mapToGlobal(self.nav_bar.menu_button.rect().bottomLeft())
        menu.exec(btn_pos)

    def _show_about_dialog(self) -> None:
        """Apresenta caixa Sobre moderna."""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "Sobre o Nimbus Browser",
            "<b>Navegador Nimbus</b> v0.2.1<br>"
            "Construído em Python com QtWebEngine (Chromium).<br><br>"
            "Moderno, rápido e com privacidade em primeiro lugar."
        )
