"""Entry point para o Navegador Nimbus."""

import os
import sys

# Porta de debug remoto Chromium para permitir DevTools completo e inspecionar elementos
os.environ.setdefault("QTWEBENGINE_REMOTE_DEBUGGING", "9222")

# Configurações de estabilidade de renderização Chromium / QtWebEngine
# Previne tela preta em GPUs integradas/drivers antigos no Windows e Linux
# Um fallback pode ser forçado pelo usuário através da variável NIMBUS_SAFE_MODE=1
safe_mode = os.environ.get("NIMBUS_SAFE_MODE", "0") == "1"

# Mitigação severa de crashes EGL/Wayland no Linux
if sys.platform.startswith("linux"):
    os.environ.setdefault("QT_QPA_PLATFORM", "xcb") # Força X11 ao invés de Wayland (evita falha de EGL nativa)
    if safe_mode:
        os.environ["QT_OPENGL"] = "software"
        os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"

if sys.platform.startswith("win"):
    if safe_mode:
        # Fallback extremo para software rasterizer (CPU) se D3D11 falhar
        os.environ["QT_OPENGL"] = "software"
    else:
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
        "--ignore-gpu-blocklist",
    ]

    if safe_mode:
        # Desliga totalmente a composição e a GPU no nível do Chromium
        chrome_flags.extend([
            "--disable-gpu",
            "--disable-gpu-compositing",
            "--disable-software-rasterizer",
        ])
    else:
        chrome_flags.append("--enable-zero-copy")

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
