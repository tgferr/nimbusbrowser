"""Testes para resolução de favicons."""

import pytest
from nimbus.engine.favicon_service import FaviconService


def test_resolve_target_url():
    service = FaviconService()
    # Href absoluto
    assert service._resolve_target_url("https://example.com", "https://cdn.example.com/icon.png") == "https://cdn.example.com/icon.png"

    # Href relativo
    assert service._resolve_target_url("https://example.com/news", "/static/fav.ico") == "https://example.com/static/fav.ico"

    # Sem href (fallback raiz)
    assert service._resolve_target_url("https://example.com/sub/page", None) == "https://example.com/favicon.ico"


def test_parse_data_uri():
    service = FaviconService()
    data_uri = "data:text/plain;utf-8,hello_world"
    res = service._parse_data_uri(data_uri)
    assert res == b"hello_world"

    # Base64
    data_b64 = "data:image/png;base64,aGVsbG8="
    assert service._parse_data_uri(data_b64) == b"hello"
