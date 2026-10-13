"""Janela principal do Navegador Nimbus em PySide6."""

from typing import Optional
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineCore import QWebEngineProfile
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTabBar,
    QTabWidget,
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

        self._setup_window()
        self._setup_ui()
        self._setup_initial_tab()

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

        # Barra de Navegação
        self.nav_bar = NavigationBar(self)
        self.nav_bar.back_requested.connect(self._on_back)
        self.nav_bar.forward_requested.connect(self._on_forward)
        self.nav_bar.reload_requested.connect(self._on_reload)
        self.nav_bar.home_requested.connect(self._on_home)
        self.nav_bar.url_submitted.connect(self._on_navigate_to_url)
        root_layout.addWidget(self.nav_bar)

        # Barra de Progresso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName("ProgressBar")
        self.progress_bar.setFixedHeight(2)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        root_layout.addWidget(self.progress_bar)

        # Tab Widget
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)

        # Botão '+' para nova aba na barra de abas
        new_tab_btn = QPushButton("+")
        new_tab_btn.setObjectName("NewTabButton")
        new_tab_btn.setToolTip("Abrir nova aba")
        new_tab_btn.clicked.connect(lambda: self.create_new_tab(self._config.default_home_url))
        self.tab_widget.setCornerWidget(new_tab_btn)

        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self.tab_widget.tabCloseRequested.connect(self._on_close_tab)
        root_layout.addWidget(self.tab_widget)

    def _setup_initial_tab(self) -> None:
        self.create_new_tab(self._config.default_home_url)

    def create_new_tab(self, url: str) -> NimbusWebView:
        """Cria e anexa uma nova aba de navegação."""
        tab_model = self._tab_manager.add_tab(url=url, title="Nova Aba")
        web_view = NimbusWebView(
            tab_id=tab_model.id,
            profile=self._profile,
            config=self._config,
            parent=self.tab_widget,
        )

        # Conexão de sinais do WebView
        web_view.title_updated.connect(lambda title, w=web_view: self._update_tab_title(w, title))
        web_view.url_updated.connect(lambda qurl, w=web_view: self._update_tab_url(w, qurl))
        web_view.loading_progress.connect(self._update_progress)
        web_view.favicon_updated.connect(lambda icon, w=web_view: self._update_tab_favicon(w, icon))

        # Adiciona aba visual
        idx = self.tab_widget.addTab(web_view, "Nova Aba")
        self.tab_widget.setCurrentIndex(idx)

        # Navega para a URL
        target_url = normalize_input_url(url)
        web_view.setUrl(QUrl(target_url))
        return web_view

    def get_current_web_view(self) -> Optional[NimbusWebView]:
        """Retorna o WebView da aba ativa no momento."""
        current_widget = self.tab_widget.currentWidget()
        if isinstance(current_widget, NimbusWebView):
            return current_widget
        return None

    def _on_tab_changed(self, index: int) -> None:
        if index < 0:
            return
        widget = self.tab_widget.widget(index)
        if isinstance(widget, NimbusWebView):
            self._tab_manager.set_active(widget.tab_id)
            self.nav_bar.set_url(widget.url().toString())
            self.nav_bar.update_navigation_state(
                widget.history().canGoBack(),
                widget.history().canGoForward(),
            )

    def _on_close_tab(self, index: int) -> None:
        if self.tab_widget.count() <= 1:
            # Se for a última aba, fecha a janela
            self.close()
            return

        widget = self.tab_widget.widget(index)
        if isinstance(widget, NimbusWebView):
            self._tab_manager.remove_tab(widget.tab_id)
            self.tab_widget.removeTab(index)
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
        idx = self.tab_widget.indexOf(web_view)
        if idx != -1:
            self.tab_widget.setTabText(idx, title)

    def _update_tab_url(self, web_view: NimbusWebView, qurl: QUrl) -> None:
        if web_view == self.get_current_web_view():
            self.nav_bar.set_url(qurl.toString())
            self.nav_bar.update_navigation_state(
                web_view.history().canGoBack(),
                web_view.history().canGoForward(),
            )

    def _update_tab_favicon(self, web_view: NimbusWebView, icon: QIcon) -> None:
        idx = self.tab_widget.indexOf(web_view)
        if idx != -1 and not icon.isNull():
            self.tab_widget.setTabIcon(idx, icon)

    def _update_progress(self, progress: int) -> None:
        if progress < 100:
            self.progress_bar.setValue(progress)
            self.progress_bar.show()
        else:
            self.progress_bar.hide()
