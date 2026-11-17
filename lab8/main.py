def get_currencies(currencies_ids_lst: list) -> list:
    """Получает курсы валют с сайта ЦБ РФ по списку ID."""
    import requests
    from xml.etree import ElementTree as ET

    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    result = []

    root = ET.fromstring(response.content)
    valutes = root.findall("Valute")

    for valute_node in valutes:
        valute_id = valute_node.get('ID')
        if str(valute_id) not in currencies_ids_lst:
            continue

        valute = {}
        name = valute_node.find('Name').text
        value_raw = valute_node.find('Value').text
        char_code = valute_node.find('CharCode').text
        nominal = valute_node.find('Nominal').text

        # Приводим значение к виду (целая_часть, дробная_часть)
        value_normalized = value_raw.replace(',', '.')
        parts = value_normalized.split('.')
        int_part = parts[0]
        frac_part = parts[1] if len(parts) > 1 else '0'

        valute[char_code] = (name, (int_part, frac_part), nominal)
        result.append(valute)

    return result


class SingletonMeta(type):
    """Метакласс, гарантирующий создание только одного экземпляра класса."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class CurrenciesLst(metaclass=SingletonMeta):
    """Класс-одиночка для работы с курсами валют ЦБ РФ."""

    def __init__(self, min_interval=1.0):
        self.__cur_lst = []
        self.__min_interval = min_interval
        self.__last_request_time = 0.0

    # ---------- Геттеры и сеттеры ----------
    def get_cur_lst(self):
        return self.__cur_lst

    def set_cur_lst(self, value):
        self.__cur_lst = value

    def get_min_interval(self):
        return self.__min_interval

    def set_min_interval(self, value):
        self.__min_interval = value

    # ---------- Основная логика ----------
    def fetch_data(self, ids_list):
        """Загружает данные о курсах с учётом ограничения частоты запросов."""
        import time

        current_time = time.time()
        elapsed = current_time - self.__last_request_time

        if elapsed < self.__min_interval:
            time.sleep(self.__min_interval - elapsed)

        self.__last_request_time = time.time()
        self.__cur_lst = get_currencies(ids_list)
        return self.__cur_lst

    def visualize_currencies(self):
        """Строит столбчатую диаграмму курсов и сохраняет в файл currencies.jpg."""
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 5))

        currency_codes = []
        currency_values = []

        for item in self.__cur_lst:
            for code, data in item.items():
                currency_codes.append(code)

                int_part, frac_part = data[1]
                value = float(f"{int_part}.{frac_part}")

                nominal = float(data[2])
                if nominal != 1:
                    value = value / nominal

                currency_values.append(value)

        ax.bar(currency_codes, currency_values, color='tab:blue')
        ax.set_ylabel('Курс (руб.)')
        ax.set_title('Курсы валют ЦБ РФ')

        for idx, val in enumerate(currency_values):
            ax.text(idx, val, f'{val:.2f}', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig('currencies.jpg')
        plt.close(fig)
        print('График сохранён в файл currencies.jpg')


if __name__ == '__main__':
    cur = CurrenciesLst(min_interval=1.0)
    data = cur.fetch_data(['R01035', 'R01335', 'R01700J'])
    if data:
        print(data)
    cur.visualize_currencies()
