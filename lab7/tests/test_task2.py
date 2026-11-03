import pytest
from decimal import Decimal
from datetime import date
from app.exceptions import ValidationError
from app.models import Currency, Rate
from app.providers import CbrXmlProvider

def test_num_code_valid():
    assert Currency("USD", "Доллар", num_code="840").num_code == "840"

def test_num_code_invalid():
    with pytest.raises(ValidationError):
        Currency("USD", "Доллар", num_code="84")
    with pytest.raises(ValidationError):
        Currency("USD", "Доллар", num_code="8A0")

def test_rate_sorting():
    day = date(2026, 10, 27)
    jpy = Rate("JPY", "Иена", 100, Decimal("53.0"), day)
    usd = Rate("USD", "Доллар", 1, Decimal("80.5"), day)
    assert jpy < usd
    assert sorted([usd, jpy]) == [jpy, usd]

def test_parse_num_code():
    xml_str = """<?xml version="1.0" encoding="windows-1251"?>
    <ValCurs Date="27.10.2026">
    <Valute><NumCode>840</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal>
    <Name>Доллар США</Name><Value>80,5</Value></Valute>
    </ValCurs>"""
    # Кодируем строку в байты, чтобы передать в парсер
    xml = xml_str.encode("windows-1251")
    
    rates = CbrXmlProvider.parse(xml)
    assert rates["USD"].num_code == "840"
    