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
    background-color: #0F1115;
}

QWidget#CentralWidget {
    background-color: #0F1115;
}

/* Barra de Topo & Navegação */
QWidget#TopBarContainer {
    background-color: #0B0B0D;
    border-bottom: 1px solid #1C1D24;
}

/* Botões de Ação Redondos com Feedback */
QPushButton.NavButton {
    background-color: transparent;
    color: #B7C0CC;
    border: none;
    border-radius: 17px;
    font-size: 15px;
    font-weight: bold;
    min-width: 34px;
    max-width: 34px;
    min-height: 34px;
    max-height: 34px;
}

QPushButton.NavButton:hover {
    background-color: #202127;
    color: #F2F5F8;
}

QPushButton.NavButton:pressed {
    background-color: #2C2D35;
}

QPushButton.NavButton:disabled {
    color: #4A4D57;
}

/* Campo de URL / Pesquisa */
QLineEdit#UrlInput {
    background-color: #1C1B22;
    color: #F2F5F8;
    border: 1px solid #3A3940;
    border-radius: 16px;
    padding: 6px 14px;
    font-size: 13px;
    selection-background-color: #0A84FF;
}

QLineEdit#UrlInput:focus {
    border: 1px solid #0A84FF;
    background-color: #212028;
}

/* Botão Ir / Busca */
QPushButton#GoButton {
    background-color: #0A84FF;
    color: #FFFFFF;
    border: none;
    border-radius: 15px;
    font-weight: bold;
    min-width: 30px;
    max-width: 30px;
    min-height: 30px;
    max-height: 30px;
}

QPushButton#GoButton:hover {
    background-color: #0070E0;
}

QPushButton#GoButton:pressed {
    background-color: #005BB5;
}

/* Barra de Abas */
QTabWidget::pane {
    border: none;
    background-color: #0F1115;
}

QTabBar::tab {
    background-color: #111216;
    color: #B7C0CC;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 8px 16px;
    min-width: 140px;
    max-width: 220px;
    margin-right: 2px;
}

QTabBar::tab:hover {
    background-color: #1A1B20;
    color: #F2F5F8;
}

QTabBar::tab:selected {
    background-color: #14151A;
    color: #F2F5F8;
    border-bottom: 2px solid #0A84FF;
}

/* Botão de Fechar Aba */
QPushButton.CloseTabButton {
    background-color: transparent;
    color: #B7C0CC;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    min-width: 18px;
    max-width: 18px;
    min-height: 18px;
    max-height: 18px;
}

QPushButton.CloseTabButton:hover {
    background-color: #383A42;
    color: #FF5555;
}

/* Botão Nova Aba '+' */
QPushButton#NewTabButton {
    background-color: transparent;
    color: #B7C0CC;
    border: none;
    border-radius: 14px;
    font-size: 18px;
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
}

QPushButton#NewTabButton:hover {
    background-color: #202127;
    color: #F2F5F8;
}

/* Barra de Progresso Sutil */
QProgressBar#ProgressBar {
    background-color: transparent;
    border: none;
    max-height: 2px;
}

QProgressBar#ProgressBar::chunk {
    background-color: #0A84FF;
}
"""
