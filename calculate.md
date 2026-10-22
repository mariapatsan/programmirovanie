# Лабораторная работа

Выполнила: Пацан Мария, 2ПОО

calculate:
``` python
"""Модуль деления с настраиваемой точностью и логированием.

Логирование ведётся через именованный логгер 'calculate'.
Глобальная конфигурация: уровень ERROR, формат включает время,
имя логгера, уровень и текст сообщения.
"""

import configparser
import logging

LOGGER_NAME = "calculate"
logger = logging.getLogger(LOGGER_NAME)
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

MIN_EPSILON = 10 ** -9
MAX_EPSILON = 10 ** -1
DEFAULT_EPSILON = 0.0001

DEFAULT_SETTINGS_FILE = "settings.ini"
DEFAULT_SECTION = "settings"
DEFAULT_OPTION = "epsilon"


def validate_epsilon(epsilon):
    """Проверяет, что epsilon — число и попадает в допустимый диапазон."""
    if not isinstance(epsilon, (int, float)):
        raise TypeError("epsilon должен быть числом")

    if not (MIN_EPSILON <= epsilon <= MAX_EPSILON):
        raise ValueError(
            f"epsilon должен быть в диапазоне "
            f"{MIN_EPSILON} <= epsilon <= {MAX_EPSILON}"
        )


def calculate(op1, op2, *, epsilon=DEFAULT_EPSILON):
    """
    Функция 1.
    Делит op1 на op2 и округляет результат с точностью epsilon.
    epsilon — ключевой аргумент.
    """
    validate_epsilon(epsilon)

    if op2 == 0:
        logger.error("Деление на ноль: op1=%r, op2=%r", op1, op2)
        raise ZeroDivisionError("Деление на ноль")

    result = op1 / op2

    # Округление до ближайшего значения, кратного epsilon
    return round(result / epsilon) * epsilon


def load_params(
    filename=DEFAULT_SETTINGS_FILE,
    section=DEFAULT_SECTION,
    option=DEFAULT_OPTION,
):
    """
    Функция 2.
    Считывает epsilon из settings.ini и устанавливает его
    значением по умолчанию для calculate.
    """
    parser = configparser.ConfigParser()
    read_files = parser.read(filename, encoding="utf-8")

    if not read_files:
        logger.critical(
            "Файл %r не найден или недоступен для чтения", filename
        )
        raise FileNotFoundError(
            f"Файл {filename!r} не найден или недоступен для чтения"
        )

    if not parser.has_section(section):
        raise KeyError(f"В файле нет секции [{section}]")

    if not parser.has_option(section, option):
        raise KeyError(f"В секции [{section}] нет параметра {option!r}")

    raw_value = parser.get(section, option)

    try:
        epsilon = parser.getfloat(section, option)
    except ValueError as exc:
        raise ValueError(
            f"Параметр {option!r} должен быть числом, получено {raw_value!r}"
        ) from exc

    validate_epsilon(epsilon)

    # Меняем значение по умолчанию для calculate
    if calculate.__kwdefaults__ is None:
        calculate.__kwdefaults__ = {}
    calculate.__kwdefaults__["epsilon"] = epsilon

    return epsilon
```

settings.ini:
``` python
[settings]
epsilon = 0.001
```

test:
``` python
import logging
import os
import tempfile
import unittest

from calc import calculate, load_params, logger


class TestCalculate(unittest.TestCase):

    def test_int_operands(self):
        self.assertAlmostEqual(calculate(10, 2, epsilon=0.001), 5.0)

    def test_float_operands(self):
        self.assertAlmostEqual(calculate(1.5, 0.5, epsilon=0.001), 3.0)

    def test_epsilon_0_1(self):
        self.assertAlmostEqual(calculate(1, 3, epsilon=0.1), 0.3, places=10)

    def test_epsilon_0_001(self):
        self.assertAlmostEqual(calculate(1, 3, epsilon=0.001), 0.333, places=10)

    def test_epsilon_0_5_invalid(self):
        with self.assertRaises(ValueError):
            calculate(1, 3, epsilon=0.5)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate(1, 0, epsilon=0.001)

    def test_epsilon_zero_invalid(self):
        with self.assertRaises(ValueError):
            calculate(1, 2, epsilon=0)

    def test_division_by_zero_logs_error(self):
        with self.assertLogs(logger, level=logging.ERROR) as cm:
            with self.assertRaises(ZeroDivisionError):
                calculate(1, 0, epsilon=0.001)

        self.assertEqual(len(cm.records), 1)
        record = cm.records[0]
        self.assertEqual(record.levelno, logging.ERROR)
        self.assertEqual(record.levelname, "ERROR")
        self.assertEqual(record.name, "calculate")
        self.assertIn("Деление на ноль", record.getMessage())


class TestLoadParams(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "settings.ini")
        self.old_default = calculate.__kwdefaults__["epsilon"]

    def tearDown(self):
        calculate.__kwdefaults__["epsilon"] = self.old_default
        self.tmp.cleanup()

    def _write_settings(self, text):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(text)

    def test_load_valid_epsilon(self):
        self._write_settings("[settings]\nepsilon = 0.001\n")

        epsilon = load_params(self.path)

        self.assertEqual(epsilon, 0.001)
        self.assertAlmostEqual(calculate(1, 3), 0.333, places=10)

    def test_file_not_found(self):
        missing_path = os.path.join(self.tmp.name, "missing.ini")

        with self.assertRaises(FileNotFoundError):
            load_params(missing_path)

    def test_missing_file_logs_critical(self):
        missing_path = os.path.join(self.tmp.name, "missing.ini")

        with self.assertLogs(logger, level=logging.CRITICAL) as cm:
            with self.assertRaises(FileNotFoundError):
                load_params(missing_path)

        self.assertEqual(len(cm.records), 1)
        record = cm.records[0]
        self.assertEqual(record.levelno, logging.CRITICAL)
        self.assertEqual(record.levelname, "CRITICAL")
        self.assertEqual(record.name, "calculate")
        message = record.getMessage()
        self.assertIn("не найден", message)
        self.assertIn(missing_path, message)

    def test_epsilon_in_range(self):
        self._write_settings("[settings]\nepsilon = 0.1\n")
        self.assertEqual(load_params(self.path), 0.1)

    def test_epsilon_lower_bound(self):
        self._write_settings("[settings]\nepsilon = 0.000000001\n")
        self.assertEqual(load_params(self.path), 10 ** -9)

    def test_epsilon_out_of_range(self):
        self._write_settings("[settings]\nepsilon = 0.5\n")
        with self.assertRaises(ValueError):
            load_params(self.path)

    def test_invalid_number_format(self):
        self._write_settings("[settings]\nepsilon = abc\n")
        with self.assertRaises(ValueError):
            load_params(self.path)

    def test_missing_section(self):
        self._write_settings("[other]\nepsilon = 0.001\n")
        with self.assertRaises(KeyError):
            load_params(self.path)

    def test_missing_option(self):
        self._write_settings("[settings]\nother = 0.001\n")
        with self.assertRaises(KeyError):
            load_params(self.path)


if __name__ == "__main__":
    unittest.main()
```
