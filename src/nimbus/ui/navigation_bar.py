"""Barra de navegação contendo botões Voltar, Avançar, Recarregar, Home e URL."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)


class NavigationBar(QWidget):
    """Barra de navegação desacoplada."""

    back_requested = Signal()
    forward_requested = Signal()
    reload_requested = Signal()
    home_requested = Signal()
    url_submitted = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("TopBarContainer")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(6)

        # Botão Voltar (←)
        self.back_button = QPushButton("◀")
        self.back_button.setProperty("class", "NavButton")
        self.back_button.setToolTip("Voltar")
        self.back_button.clicked.connect(self.back_requested.emit)
        layout.addWidget(self.back_button)

        # Botão Avançar (→)
        self.forward_button = QPushButton("▶")
        self.forward_button.setProperty("class", "NavButton")
        self.forward_button.setToolTip("Avançar")
        self.forward_button.clicked.connect(self.forward_requested.emit)
        layout.addWidget(self.forward_button)

        # Botão Recarregar (⟳)
        self.reload_button = QPushButton("⟳")
        self.reload_button.setProperty("class", "NavButton")
        self.reload_button.setToolTip("Recarregar página")
        self.reload_button.clicked.connect(self.reload_requested.emit)
        layout.addWidget(self.reload_button)

        # Botão Home (⌂)
        self.home_button = QPushButton("⌂")
        self.home_button.setProperty("class", "NavButton")
        self.home_button.setToolTip("Página Inicial")
        self.home_button.clicked.connect(self.home_requested.emit)
        layout.addWidget(self.home_button)

        # Campo de URL / Pesquisa
        self.url_input = QLineEdit()
        self.url_input.setObjectName("UrlInput")
        self.url_input.setPlaceholderText("Pesquise ou digite um endereço da Web")
        self.url_input.returnPressed.connect(self._on_submit)
        layout.addWidget(self.url_input)

        # Botão Ir (➔)
        self.go_button = QPushButton("➔")
        self.go_button.setObjectName("GoButton")
        self.go_button.setToolTip("Navegar")
        self.go_button.clicked.connect(self._on_submit)
        layout.addWidget(self.go_button)

    def _on_submit(self) -> None:
        text = self.url_input.text().strip()
        if text:
            self.url_submitted.emit(text)

    def set_url(self, url: str) -> None:
        """Atualiza o texto da barra de URL sem disparar submit."""
        if not self.url_input.hasFocus():
            self.url_input.setText(url)

    def update_navigation_state(self, can_go_back: bool, can_go_forward: bool) -> None:
        """Habilita/desabilita botões conforme histórico."""
        self.back_button.setEnabled(can_go_back)
        self.forward_button.setEnabled(can_go_forward)
