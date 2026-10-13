"""Estilos QSS (Qt Style Sheet) fiéis ao tema Dark do Nimbus WPF original."""

# Paleta extraída diretamente de MainWindow.xaml:
# WindowBgBrush: #050506 / #0F1115
# TopBarBrush: #0B0B0D
# TabBgBrush: #111216
# TabHoverBrush: #1A1B20
# TabSelectedBrush: #14151A
# TextBrush: #F2F5F8
# MutedTextBrush: #B7C0CC
# UrlBgBrush: #1C1B22
# UrlBorderBrush: #3A3940
# AccentBrush: #0A84FF

NIMBUS_DARK_THEME_QSS = """
QMainWindow {
    background-color: #0b0c10;
}

QWidget#CentralWidget {
    background-color: #0b0c10;
}

/* Faixa Superior de Abas (Estilo Chrome / Arc) */
QWidget#TabHeaderContainer {
    background-color: #0b0c10;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

/* Barra de Topo & Navegação com Glassmorphism */
QWidget#TopBarContainer {
    background-color: #14171f;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 3px 10px;
}

/* Botões de Ação Redondos com Microinterações */
QPushButton.NavButton {
    background-color: transparent;
    color: #9aa5b5;
    border: none;
    border-radius: 17px;
    font-size: 14px;
    min-width: 34px;
    max-width: 34px;
    min-height: 34px;
    max-height: 34px;
}

QPushButton.NavButton:hover {
    background-color: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}

QPushButton.NavButton:pressed {
    background-color: rgba(255, 255, 255, 0.14);
}

QPushButton.NavButton:disabled {
    color: #3f444e;
}

/* Campo de URL com Pill Design Moderno */
QLineEdit#UrlInput {
    background-color: #1c202a;
    color: #f2f5f8;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 18px;
    padding: 6px 18px;
    font-size: 13px;
    selection-background-color: #0a84ff;
}

QLineEdit#UrlInput:focus {
    border: 1px solid #0a84ff;
    background-color: #212632;
    box-shadow: 0 0 10px rgba(10, 132, 255, 0.3);
}

/* Botão Ir / Busca */
QPushButton#GoButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0a84ff, stop:1 #006ee6);
    color: #ffffff;
    border: none;
    border-radius: 16px;
    font-weight: bold;
    font-size: 13px;
    min-width: 32px;
    max-width: 32px;
    min-height: 32px;
    max-height: 32px;
}

QPushButton#GoButton:hover {
    background: #0077f0;
}

QPushButton#GoButton:pressed {
    background: #005bb5;
}

/* Separador sutil de navegação */
QWidget#NavSeparator {
    background-color: rgba(255, 255, 255, 0.1);
    max-width: 1px;
    margin: 6px 4px;
}

/* QTabBar customizada (Chrome Tabs) */
QTabBar#NimbusTabBar {
    background: transparent;
    border: none;
}

QTabBar#NimbusTabBar::tab {
    background: #14171f;
    color: #8e99a8;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 7px 8px 7px 14px;
    min-width: 140px;
    max-width: 220px;
    margin-right: 4px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: none;
}

QTabBar#NimbusTabBar::tab:hover {
    background: #1a1e27;
    color: #f2f5f8;
}

QTabBar#NimbusTabBar::tab:selected {
    background: #1e222b;
    color: #ffffff;
    border-top: 2px solid #0a84ff;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid #1e222b;
}

/* Botão de Fechar Aba 'X' posicionado harmonicamente à esquerda do limite da aba */
QPushButton.TabCloseButton {
    background-color: transparent;
    color: #8e99a8;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    min-width: 18px;
    max-width: 18px;
    min-height: 18px;
    max-height: 18px;
    margin-left: 4px;
    margin-right: 8px;
}

QPushButton.TabCloseButton:hover {
    background-color: rgba(255, 69, 58, 0.3);
    color: #ff453a;
}

QPushButton.TabCloseButton:pressed {
    background-color: rgba(255, 69, 58, 0.5);
    color: #ffffff;
}

/* Menu de Contexto Escuro M2 */
QMenu#NimbusContextMenu {
    background-color: #161922;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 6px;
    color: #f2f5f8;
    font-size: 13px;
}

QMenu#NimbusContextMenu::item {
    background-color: transparent;
    padding: 7px 22px 7px 12px;
    border-radius: 8px;
    margin: 2px 0px;
}

QMenu#NimbusContextMenu::item:selected {
    background-color: #0a84ff;
    color: #ffffff;
}

QMenu#NimbusContextMenu::item:disabled {
    color: #555c68;
}

QMenu#NimbusContextMenu::separator {
    height: 1px;
    background-color: rgba(255, 255, 255, 0.08);
    margin: 4px 6px;
}

/* Botão Nova Aba '+' ao lado das abas */
QPushButton#NewTabButton {
    background-color: transparent;
    color: #9aa5b5;
    border: none;
    border-radius: 14px;
    font-size: 18px;
    font-weight: 300;
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
    margin-bottom: 2px;
}

QPushButton#NewTabButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #ffffff;
}

QPushButton#NewTabButton:pressed {
    background-color: rgba(255, 255, 255, 0.16);
}

/* Container de Conteúdo */
QStackedWidget#WebContentStack {
    background-color: #0b0c10;
    border: none;
}

/* Barra de Progresso com Gradiente */
QProgressBar#ProgressBar {
    background-color: transparent;
    border: none;
    max-height: 2px;
}

QProgressBar#ProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0a84ff, stop:1 #5e5ce6);
}
"""
