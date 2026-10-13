"""Definições e constantes centrais do Navegador Nimbus."""

import sys
from dataclasses import dataclass
from pathlib import Path


def _resolve_assets_dir() -> Path:
    """
    Resolve o diretório de assets de forma compatível com:
    1. Desenvolvimento local (Python puro / venv)
    2. Binário empacotado PyInstaller (Windows .exe e Linux ELF)
    """
    # PyInstaller define sys.frozen = True e sys._MEIPASS aponta para a pasta descompactada
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            meipass_assets = Path(sys._MEIPASS) / "assets"
            if meipass_assets.exists():
                return meipass_assets

        # No modo --onedir, sys.executable fica em dist/Nimbus/Nimbus e os assets podem estar em _internal/assets ou assets/
        exe_dir = Path(sys.executable).resolve().parent
        for candidate in (exe_dir / "assets", exe_dir / "_internal" / "assets"):
            if candidate.exists():
                return candidate

    # Modo desenvolvimento (src/nimbus/core/constants.py -> raiz/assets)
    dev_base = Path(__file__).resolve().parent.parent.parent.parent
    dev_assets = dev_base / "assets"
    if dev_assets.exists():
        return dev_assets

    return dev_base / "assets"


# Caminhos de Assets
ASSETS_DIR = _resolve_assets_dir()
ICON_PATH = ASSETS_DIR / "nimbus_icon.ico"
OFFLINE_HOME_PATH = ASSETS_DIR / "offline_home.html"
HOME_HTML_PATH = ASSETS_DIR / "home.html"


def get_default_home_url() -> str:
    """Retorna a URL inicial resolvida em runtime."""
    assets = _resolve_assets_dir()
    home_file = assets / "home.html"
    if home_file.exists():
        return home_file.as_uri()
    return "about:blank"


# URLs Padrão (Local First)
DEFAULT_HOME_URL = get_default_home_url()
NEW_TAB_URL = DEFAULT_HOME_URL


@dataclass(frozen=True)
class BrowserConfig:
    """Configurações imutáveis do navegador."""
    window_title: str = "Navegador Nimbus"
    initial_width: int = 1200
    initial_height: int = 760
    min_width: int = 900
    min_height: int = 560
    default_home_url: str = DEFAULT_HOME_URL
    title_max_length: int = 25
    enable_javascript: bool = True
    enable_local_storage: bool = True


def normalize_input_url(input_url: str) -> str:
    """
    Normaliza a URL digitada pelo usuário, adicionando https:// se necessário
    ou redirecionando para busca se não for um domínio válido.
    """
    url = input_url.strip()
    if not url:
        return DEFAULT_HOME_URL

    if url.startswith(("http://", "https://", "file://", "about:")):
        return url

    # Se contém ponto e sem espaços, presume domínio web
    if "." in url and " " not in url:
        return f"https://{url}"

    # Caso contrário, trata como busca web (fallback DuckDuckGo/Google)
    return f"https://duckduckgo.com/?q={url}"
