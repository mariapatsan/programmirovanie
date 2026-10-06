# Лабораторная работа

Выполнила: Пацан Мария, 2ПОО

main.py:



```python
import configparser
import math
import os


def calculate(number1, number2, epsilon=0.0001):
    """Делит number1 на number2 с точностью epsilon."""
    if number2 == 0:
        raise ZeroDivisionError("Нельзя делить на ноль")

    if not 10**-9 <= epsilon <= 10**-1:
        raise ValueError("Значение epsilon находится вне диапазона")

    answer = number1 / number2
    decimal_places = max(0, -int(math.floor(math.log10(epsilon))))
    return round(answer, decimal_places)


def load_params(filename="settings.ini"):
    """Загружает epsilon из конфигурационного файла."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл не найден: {filename}")

    settings = configparser.ConfigParser()
    settings.read(filename)

    if not settings.has_section("settings") or not settings.has_option("settings", "epsilon"):
        raise ValueError("В файле нет секции [settings] или параметра epsilon")

    try:
        epsilon = float(settings["settings"]["epsilon"])
    except ValueError:
        raise ValueError("epsilon в файле не является числом")

    if not 10**-9 <= epsilon <= 10**-1:
        raise ValueError("Значение epsilon находится вне диапазона")

    return epsilon


if __name__ == "__main__":
    epsilon = load_params()
    print(calculate(1, 2, epsilon=epsilon))
```
## Конфигурационный файл

settings.ini.

[settings]
epsilon = 0.0001
## Проверка программы

test_main.py:

``` python
import os
import unittest

from main import calculate, load_params


class TestCalculate(unittest.TestCase):

    def test_division(self):
        result = calculate(1, 2, epsilon=0.1)
        self.assertEqual(result, 0.5)

    def test_small_result(self):
        result = calculate(1, 1000, epsilon=0.001)
        self.assertEqual(result, 0.001)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate(1, 0)


class TestLoadParams(unittest.TestCase):

    def test_settings_file(self):
        self.assertTrue(os.path.exists("settings.ini"))

    def test_epsilon_value(self):
        epsilon = load_params()
        self.assertTrue(10**-9 <= epsilon <= 10**-1)

    def test_number_format(self):
        epsilon = load_params()
        self.assertIsInstance(epsilon, float)


if __name__ == "__main__":
    unittest.main()
```
