"""Teste de fumaça e integração da MainWindow do Nimbus."""

import os
import pytest

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from nimbus.ui.main_window import NimbusMainWindow
from nimbus.core.constants import BrowserConfig


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_main_window_lifecycle(qapp, qtbot):
    config = BrowserConfig(default_home_url="about:blank")
    window = NimbusMainWindow(config=config)
    qtbot.addWidget(window)

    # Verifica aba inicial
    assert window.tab_widget.count() == 1
    assert window.get_current_web_view() is not None

    # Abre nova aba
    new_web_view = window.create_new_tab("about:blank")
    assert window.tab_widget.count() == 2
    assert window.get_current_web_view() == new_web_view

    # Fecha aba
    window._on_close_tab(1)
    assert window.tab_widget.count() == 1

    # Cleanup explícito no teardown
    window.close()
    qapp.processEvents()
