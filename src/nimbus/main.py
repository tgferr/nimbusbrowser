"""Entry point para o Navegador Nimbus."""

import sys
from PySide6.QtWidgets import QApplication

from nimbus.core.constants import BrowserConfig
from nimbus.ui.main_window import NimbusMainWindow


def main() -> int:
    """Função principal que inicia a aplicação Qt."""
    app = QApplication(sys.argv)
    app.setApplicationName("Navegador Nimbus")
    app.setOrganizationName("Nimbus")

    config = BrowserConfig()
    window = NimbusMainWindow(config=config)
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
