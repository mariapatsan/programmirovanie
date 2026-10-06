# Лабораторная работа

Выполнила: Пацан Мария, 2ПОО

main.py:



```python
import configparser


def calculate(number1, number2, epsilon=0.0001):
    """Выполняет деление двух чисел."""
    if number2 == 0:
        raise ZeroDivisionError("Нельзя делить на ноль")

    if not 10**-9 <= epsilon <= 10**-1:
        raise ValueError("Значение epsilon находится вне диапазона")

    answer = number1 / number2
    return round(answer, 10)


def load_params(filename="settings.ini"):
    """Загружает epsilon из конфигурационного файла."""
    settings = configparser.ConfigParser()
    settings.read(filename)

    epsilon = float(settings["settings"]["epsilon"])

    if not 10**-9 <= epsilon <= 10**-1:
        raise ValueError("Значение epsilon находится вне диапазона")

    return epsilon


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
