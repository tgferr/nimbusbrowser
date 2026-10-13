"""Configuração global do Pytest para o Nimbus."""

import os
import pytest

# Garante modo headless offscreen para testes sem tela gráfica
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """
    QWebEngine no Linux em modo offscreen/headless dispara segfault no hook de saída da libc
    devido à destruição tardia de singletons do Chromium após o desligamento do QCoreApplication.
    Usar os._exit(exitstatus) garante saída com código de retorno preservado e sem falha de segmentação.
    """
    import os
    os._exit(exitstatus)
