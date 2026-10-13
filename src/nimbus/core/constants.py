"""Definições e constantes centrais do Navegador Nimbus."""

from dataclasses import dataclass
from pathlib import Path

# Caminhos de Assets
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ASSETS_DIR = BASE_DIR / "assets"
ICON_PATH = ASSETS_DIR / "nimbus_icon.ico"
OFFLINE_HOME_PATH = ASSETS_DIR / "offline_home.html"
HOME_HTML_PATH = ASSETS_DIR / "home.html"

# URLs Padrão (Local First)
DEFAULT_HOME_URL = HOME_HTML_PATH.as_uri() if HOME_HTML_PATH.exists() else "about:blank"
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
