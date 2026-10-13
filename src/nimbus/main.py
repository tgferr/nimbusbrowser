"""Entry point para o Navegador Nimbus."""

import os
import sys

# Porta de debug remoto Chromium para permitir DevTools completo e inspecionar elementos
os.environ.setdefault("QTWEBENGINE_REMOTE_DEBUGGING", "9222")

# Configurações de estabilidade de renderização Chromium / QtWebEngine
# Previne tela preta em GPUs integradas/drivers antigos no Windows e Linux
if sys.platform.startswith("win"):
    # Garante renderização D3D11 / ANGLE estável no Windows
    os.environ.setdefault("QT_OPENGL", "angle")
    os.environ.setdefault("QT_ANGLE_PLATFORM", "d3d11")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from nimbus.core.constants import BrowserConfig
from nimbus.ui.main_window import NimbusMainWindow


def main() -> int:
    """Função principal que inicia a aplicação Qt."""
    # Atributos de compatibilidade gráfica antes de criar QApplication
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)

    # Flags Chromium passadas via linha de comando para evitar GPU crashes no Windows
    chrome_flags = [
        "--enable-smooth-scrolling",
        "--enable-zero-copy",
        "--ignore-gpu-blocklist",
    ]
    sys_argv = sys.argv + ["--webEngineArgs"] + chrome_flags

    app = QApplication(sys_argv)
    app.setApplicationName("Navegador Nimbus")
    app.setOrganizationName("Nimbus")

    config = BrowserConfig()
    window = NimbusMainWindow(config=config)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
