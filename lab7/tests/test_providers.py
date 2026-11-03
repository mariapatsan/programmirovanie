from decimal import Decimal
import pytest
import requests
from app.exceptions import NotFoundError, ProviderError
from app.providers import CbrXmlProvider, RateProvider, StaticRateProvider

SAMPLE_XML = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="27.10.2026" name="Foreign Currency Market">
<Valute ID="R01235"><NumCode>840</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal>
<Name>Доллар США</Name><Value>80,5000</Value></Valute>
</ValCurs>""".encode("windows-1251")

def test_abstract_provider():
    with pytest.raises(TypeError):
        RateProvider()

def test_cbr_parse():
    rates = CbrXmlProvider.parse(SAMPLE_XML)
    assert rates["USD"].name == "Доллар США"

def test_cbr_network_error(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **kw: (_ for _ in ()).throw(requests.ConnectionError()))
    with pytest.raises(ProviderError):
        CbrXmlProvider().get_rates()