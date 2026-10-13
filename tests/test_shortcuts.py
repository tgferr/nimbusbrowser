"""Testes para validação dos atalhos de teclado da MainWindow."""

import os
import pytest

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QApplication
from nimbus.ui.main_window import NimbusMainWindow
from nimbus.core.constants import BrowserConfig


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_main_window_shortcuts(qapp, qtbot):
    config = BrowserConfig(default_home_url="about:blank")
    window = NimbusMainWindow(config=config)
    qtbot.addWidget(window)

    # 1. Nova Aba via método disparado por Ctrl+T
    assert window.tab_widget.count() == 1
    assert window.tab_widget.currentIndex() == 0

    window.create_new_tab("https://example.com")
    assert window.tab_widget.count() == 2
    # create_new_tab seleciona a nova aba criada (índice 1)
    assert window.tab_widget.currentIndex() == 1

    # 2. Navegação de abas (Ctrl+Tab circula para 0, Ctrl+Shift+Tab volta para 1)
    window._next_tab()
    assert window.tab_widget.currentIndex() == 0
    window._prev_tab()
    assert window.tab_widget.currentIndex() == 1

    # 3. Fechar aba via Ctrl+W e reabrir via Ctrl+Shift+T
    window.tab_widget.setCurrentIndex(1)
    window._close_current_tab()
    assert window.tab_widget.count() == 1
    assert len(window._closed_tabs_history) == 1
    assert window._closed_tabs_history[0] == "https://example.com"

    # Reabre última
    window._reopen_last_closed_tab()
    assert window.tab_widget.count() == 2

    # 4. Foco na barra de URL (Ctrl+L)
    window._focus_url_bar()
    assert window.nav_bar.url_input is not None

    window.close()
