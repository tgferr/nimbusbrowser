"""Serviço de download e resolução de favicon com fallback."""

import asyncio
from typing import Optional
from urllib.parse import urljoin, urlparse
import httpx


class FaviconService:
    """Resolve e baixa favicons via HTML, URL relativa ou fallback /favicon.ico."""

    def __init__(self, timeout: float = 3.0) -> None:
        self._timeout = timeout

    async def fetch_favicon_async(self, base_url: str, icon_href: Optional[str] = None) -> Optional[bytes]:
        """Busca favicon em background via HTTPX assíncrono."""
        if not base_url or not base_url.startswith(("http://", "https://")):
            return None

        target_url = self._resolve_target_url(base_url, icon_href)
        if not target_url:
            return None

        # Trata data: URI inline
        if target_url.startswith("data:"):
            return self._parse_data_uri(target_url)

        try:
            async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True) as client:
                response = await client.get(target_url)
                if response.status_code == 200 and response.content:
                    return response.content
        except Exception:
            # Fallback secundário direto para raiz /favicon.ico
            if not target_url.endswith("/favicon.ico"):
                return await self._fetch_root_fallback(base_url)

        return None

    def _resolve_target_url(self, base_url: str, icon_href: Optional[str]) -> Optional[str]:
        if icon_href and icon_href.strip():
            cleaned = icon_href.strip().strip('"').strip("'")
            if cleaned.startswith(("http://", "https://", "data:")):
                return cleaned
            return urljoin(base_url, cleaned)

        # Fallback raiz
        parsed = urlparse(base_url)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}/favicon.ico"
        return None

    async def _fetch_root_fallback(self, base_url: str) -> Optional[bytes]:
        parsed = urlparse(base_url)
        fallback_url = f"{parsed.scheme}://{parsed.netloc}/favicon.ico"
        try:
            async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True) as client:
                response = await client.get(fallback_url)
                if response.status_code == 200 and response.content:
                    return response.content
        except Exception:
            return None
        return None

    @staticmethod
    def _parse_data_uri(data_uri: str) -> Optional[bytes]:
        try:
            import base64
            comma_idx = data_uri.find(",")
            if comma_idx == -1:
                return None
            meta = data_uri[:comma_idx]
            payload = data_uri[comma_idx + 1:]
            if ";base64" in meta.lower():
                return base64.b64decode(payload)
            return payload.encode("utf-8")
        except Exception:
            return None
