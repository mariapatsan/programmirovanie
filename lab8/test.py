import unittest
from singleton import CurrenciesLst


class TestCurrencyService(unittest.TestCase):
    """Набор тестов для проверки класса CurrenciesLst."""

    @classmethod
    def setUpClass(cls):
        # Создаём один экземпляр на все тесты, чтобы не дёргать сервер лишний раз
        cls.service = CurrenciesLst(min_interval=0.0)

    def _get_currency_info(self, result):
        """Вспомогательный метод: достаёт код и данные валюты из результата."""
        record = result[0]
        currency_code = list(record.keys())[0]
        currency_data = record[currency_code]
        return currency_code, currency_data

    def test_wrong_id_returns_empty(self):
        """Если ID валюты неверный — результат должен быть пустым."""
        result = self.service.fetch_data(['R9999'])
        self.assertEqual(result, [])

    def test_gbp_data_is_correct(self):
        """Проверяем, что для фунта стерлингов приходят правильные данные."""
        result = self.service.fetch_data(['R01035'])
        self.assertGreater(len(result), 0)

        code, data = self._get_currency_info(result)
        self.assertEqual(code, 'GBP')

        name = data[0]
        self.assertIn('Фунт стерлингов', name)

        # Собираем курс обратно из целой и дробной частей
        rate = float(f"{data[1][0]}.{data[1][1]}")
        self.assertTrue(0 <= rate <= 999, f"Курс вне диапазона: {rate}")

    def test_kzt_data_is_correct(self):
        """Проверяем, что для казахстанского тенге приходят правильные данные."""
        result = self.service.fetch_data(['R01335'])
        self.assertGreater(len(result), 0)

        code, data = self._get_currency_info(result)
        self.assertEqual(code, 'KZT')

        name = data[0]
        self.assertIn('Тенге', name)

        rate = float(f"{data[1][0]}.{data[1][1]}")
        self.assertTrue(0 <= rate <= 999, f"Курс вне диапазона: {rate}")

    def test_singleton_returns_same_object(self):
        """Проверяем, что шаблон «Одиночка» работает: объект всегда один."""
        another_service = CurrenciesLst()
        self.assertIs(self.service, another_service)


if __name__ == '__main__':
    unittest.main()
