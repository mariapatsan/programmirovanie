import pytest
import requests
from app.exceptions import ProviderError
from app.providers import CbrXmlProvider

def test_skipped_count():
    xml = b"""<?xml version="1.0" encoding="windows-1251"?>
    <ValCurs Date="27.10.2026">
    <Valute><NumCode>840</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal>
    <Name>Dollar</Name><Value>80,5</Value></Valute>
    <Valute><CharCode>BAD</CharCode><Nominal>abc</Nominal>
    <Name>Broken</Name><Value>0</Value></Valute>
    </ValCurs>"""
    provider = CbrXmlProvider()
    rates = provider.parse(xml)
    assert "USD" in rates
    assert provider.skipped_count == 1

def test_timeout_raises_provider_error(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.Timeout("timed out")
    monkeypatch.setattr(requests, "get", fake_get)
    with pytest.raises(ProviderError):
        CbrXmlProvider(timeout=5).get_rates()
