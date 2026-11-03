import pytest
from decimal import Decimal
from app.providers import CbrJsonProvider

SAMPLE_JSON = {
    "Date": "2026-10-27T11:30:00+03:00",
    "Valute": {
        "USD": {
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 80.5,
        }
    }
}

def test_json_parse(monkeypatch):
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self): return SAMPLE_JSON

    monkeypatch.setattr("requests.get", lambda *a, **kw: FakeResponse())
    provider = CbrJsonProvider()
    rates = provider.get_rates()
    
    assert "USD" in rates
    assert rates["USD"].value == Decimal("80.5")
    assert rates["USD"].num_code == "840"