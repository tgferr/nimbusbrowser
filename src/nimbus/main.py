"""Entry point para o Navegador Nimbus."""

import os
import sys

# Porta de debug remoto Chromium para permitir DevTools completo e inspecionar elementos
os.environ.setdefault("QTWEBENGINE_REMOTE_DEBUGGING", "9222")

# Configurações de estabilidade de renderização Chromium / QtWebEngine
# Previne tela preta em GPUs integradas/drivers antigos no Windows e Linux
# Um fallback pode ser forçado pelo usuário através da variável NIMBUS_SAFE_MODE=1
safe_mode = os.environ.get("NIMBUS_SAFE_MODE", "0") == "1" or "--safe-mode" in sys.argv

# Mitigação severa de crashes EGL/Wayland/GLX no Linux
if sys.platform.startswith("linux"):
    # Garante compatibilidade gráfica mais universal no Linux em empacotamentos (.deb/.AppImage)
    os.environ.setdefault("QT_QPA_PLATFORM", "xcb") # Força X11 
    
    # Se GLX falhar no desktop environment do usuário, forçamos renderização por software nativa do Qt
    if safe_mode:
        os.environ["QT_XCB_GL_INTEGRATION"] = "none"
        os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"
        os.environ["QT_OPENGL"] = "software"

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
        # Desliga hardware acceleration e permite CPU render (SwiftShader)
        chrome_flags.extend([
            "--disable-gpu",
            "--disable-gpu-compositing",
            "--disable-d3d11",
        ])
    else:
        chrome_flags.append("--enable-zero-copy")

    sys_argv = [arg for arg in sys.argv if arg != "--safe-mode"]
    sys_argv = sys_argv + ["--webEngineArgs"] + chrome_flags

    app = QApplication(sys_argv)
    app.setApplicationName("Navegador Nimbus")
    app.setOrganizationName("Nimbus")

    config = BrowserConfig()
    window = NimbusMainWindow(config=config)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
