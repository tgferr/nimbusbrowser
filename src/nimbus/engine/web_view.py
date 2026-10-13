"""Componente de visualização web desacoplado usando PySide6 QWebEngineView."""

from typing import Callable, Optional
from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineSettings,
)
from PySide6.QtWebEngineWidgets import QWebEngineView

from nimbus.core.constants import BrowserConfig


class NimbusWebPage(QWebEnginePage):
    """Página customizada do WebEngine com políticas de segurança."""

    def __init__(self, profile: QWebEngineProfile, parent=None) -> None:
        super().__init__(profile, parent)


class NimbusWebView(QWebEngineView):
    """
    Abstração de WebView para o Nimbus.
    Equivalente limpo ao WebView2 do WPF.
    """

    # Sinais emitidos para a camada de UI
    title_updated = Signal(str)
    url_updated = Signal(QUrl)
    loading_progress = Signal(int)
    favicon_updated = Signal(QIcon)

    def __init__(
        self,
        tab_id: str,
        profile: Optional[QWebEngineProfile] = None,
        config: Optional[BrowserConfig] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.tab_id = tab_id
        self._config = config or BrowserConfig()

        # Cria a página com parent explícito no WebView para casamento de ciclo de vida
        if profile is not None:
            page = NimbusWebPage(profile, self)
            self.setPage(page)

        self._configure_settings()
        self._connect_signals()

    def _configure_settings(self) -> None:
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, self._config.enable_javascript)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, self._config.enable_local_storage)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)

    def _connect_signals(self) -> None:
        self.titleChanged.connect(self._on_title_changed)
        self.urlChanged.connect(self._on_url_changed)
        self.loadProgress.connect(self.loading_progress.emit)
        self.iconChanged.connect(self.favicon_updated.emit)

    def _on_title_changed(self, title: str) -> None:
        if not title:
            title = "Nova Aba"
        elif len(title) > self._config.title_max_length:
            title = title[: self._config.title_max_length - 3] + "..."
        self.title_updated.emit(title)

    def _on_url_changed(self, qurl: QUrl) -> None:
        self.url_updated.emit(qurl)

    def extract_favicon_href_async(self, callback: Callable[[str], None]) -> None:
        """Executa JS idêntico ao original C# para encontrar tag <link rel='icon'>."""
        js_code = """
        (function() {
            try {
                var links = document.querySelectorAll('link[rel~="icon"]');
                if (links.length > 0) return links[0].href;
                return '';
            } catch (e) { return ''; }
        })();
        """
        self.page().runJavaScript(js_code, callback)

    def dispose(self) -> None:
        """Libera determinísticamente os recursos do WebView."""
        self.stop()
        self.deleteLater()
