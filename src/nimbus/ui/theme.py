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

/* Barra de Topo & Navegação com Glassmorphism */
QWidget#TopBarContainer {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #16181f, stop:1 #101217);
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    padding: 2px 8px;
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
    background-color: #1a1d24;
    color: #f2f5f8;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 6px 16px;
    font-size: 13px;
    selection-background-color: #0a84ff;
}

QLineEdit#UrlInput:focus {
    border: 1px solid #0a84ff;
    background-color: #1e222b;
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

/* Barra de Abas Flutuantes e Modernas */
QTabWidget::pane {
    border: none;
    background-color: #0b0c10;
}

QTabBar {
    background: transparent;
}

QTabBar::tab {
    background: #14171d;
    color: #8e99a8;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    padding: 8px 18px;
    min-width: 140px;
    max-width: 220px;
    margin-right: 4px;
    margin-top: 4px;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-bottom: none;
}

QTabBar::tab:hover {
    background: #1c2028;
    color: #f2f5f8;
}

QTabBar::tab:selected {
    background: #1e222a;
    color: #ffffff;
    border-top: 2px solid #0a84ff;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Botão de Fechar Aba */
QPushButton.CloseTabButton {
    background-color: transparent;
    color: #8e99a8;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    min-width: 18px;
    max-width: 18px;
    min-height: 18px;
    max-height: 18px;
}

QPushButton.CloseTabButton:hover {
    background-color: rgba(255, 69, 58, 0.2);
    color: #ff453a;
}

/* Botão Nova Aba '+' */
QPushButton#NewTabButton {
    background-color: transparent;
    color: #9aa5b5;
    border: none;
    border-radius: 14px;
    font-size: 18px;
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
    margin-left: 4px;
}

QPushButton#NewTabButton:hover {
    background-color: rgba(255, 255, 255, 0.08);
    color: #ffffff;
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
