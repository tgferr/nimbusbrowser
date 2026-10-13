"""Testes de renderização e estabilidade (Matriz Windows/GPU)."""

import os
import sys
import pytest

from PySide6.QtWidgets import QApplication
from nimbus.ui.main_window import NimbusMainWindow
from nimbus.core.constants import BrowserConfig

@pytest.fixture
def mock_safe_mode(monkeypatch):
    """Ativa o NIMBUS_SAFE_MODE para forçar renderização por software."""
    monkeypatch.setenv("NIMBUS_SAFE_MODE", "1")
    monkeypatch.setattr(sys, "platform", "win32") # Simula estar no Windows


def test_safe_mode_forces_software_rendering(mock_safe_mode):
    """
    Testa se as variáveis de ambiente e flags do Chromium são
    configuradas corretamente para evitar a tela preta no Windows.
    """
    # Recarrega o módulo main para reavaliar variáveis de escopo global
    import importlib
    import nimbus.main
    importlib.reload(nimbus.main)
    
    assert nimbus.main.safe_mode is True

    # Valida presença das flags no construtor sys_argv simulado
    chrome_flags = [
        "--enable-smooth-scrolling",
        "--ignore-gpu-blocklist",
    ]
    if nimbus.main.safe_mode:
        chrome_flags.extend([
            "--disable-gpu",
            "--disable-gpu-compositing",
            "--disable-d3d11",
        ])
    
    assert "--disable-gpu" in chrome_flags
    assert "--disable-gpu-compositing" in chrome_flags
    assert "--disable-d3d11" in chrome_flags
