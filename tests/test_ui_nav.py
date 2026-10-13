"""Testes de interface com pytest-qt em ambiente offscreen."""

import os
import pytest

# Força plataforma offscreen caso não haja display gráfico ativo
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from nimbus.ui.navigation_bar import NavigationBar
from nimbus.core.constants import DEFAULT_HOME_URL


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_navigation_bar_events(qapp, qtbot):
    nav_bar = NavigationBar()
    qtbot.addWidget(nav_bar)

    signals_received = {
        "back": False,
        "forward": False,
        "reload": False,
        "home": False,
        "url": None,
    }

    nav_bar.back_requested.connect(lambda: signals_received.update({"back": True}))
    nav_bar.forward_requested.connect(lambda: signals_received.update({"forward": True}))
    nav_bar.reload_requested.connect(lambda: signals_received.update({"reload": True}))
    nav_bar.home_requested.connect(lambda: signals_received.update({"home": True}))
    nav_bar.url_submitted.connect(lambda u: signals_received.update({"url": u}))

    # Clica nos botões
    qtbot.mouseClick(nav_bar.back_button, Qt.MouseButton.LeftButton)
    assert signals_received["back"] is True

    qtbot.mouseClick(nav_bar.forward_button, Qt.MouseButton.LeftButton)
    assert signals_received["forward"] is True

    qtbot.mouseClick(nav_bar.reload_button, Qt.MouseButton.LeftButton)
    assert signals_received["reload"] is True

    qtbot.mouseClick(nav_bar.home_button, Qt.MouseButton.LeftButton)
    assert signals_received["home"] is True

    # Digita URL e clica Go
    nav_bar.url_input.setText("example.com")
    qtbot.mouseClick(nav_bar.go_button, Qt.MouseButton.LeftButton)
    assert signals_received["url"] == "example.com"
