import requests  # вызов библиотеки requests для получения данных с сайта
import consts  # вызов констант такой как keys, описанный в файле main
import json  # вызов библиотеки json для преобразования данных
import decimal  # вызов decimal для корректного расчета

"""
 использовала библиотеку decimal для корректного расчета данных
"""


class APIException(
    Exception
):  # собственный класс исключений, является дочерним общего класса Исключений
    ...


class CryptoConverter:  # создание класса с исключениями
    def __init__(self): ...

    @staticmethod
    def exceptions(
        quote: str, base: str, amount: str
    ):  # входные данные передаются в типе данных str
        if (
            quote == base
        ):  # если введенные типы валют одинаковы, срабатывает исключения одинаковых типов
            raise APIException(
                f"Невозможно перевести валюты одинакового типа: Тип введеной валюты - {base}."
            )

        try:
            base_ticker = consts.keys[base]
        except (
            KeyError
        ):  # вызывание исключения KeyError если ключа в файле consts.keys нет, ошибка в названии ключа
            raise APIException(
                f"Нет информации про данный тип валют: Тип валюты - {base}."
            )

        try:
            quote_ticker = consts.keys[quote]
        except (
            KeyError
        ):  # вызывание исключения KeyError если ключа в файле consts.keys нет, ошибка в названии ключа
            raise APIException(
                f"Нет информации про данный тип валют: Тип валюты - {quote}."
            )

        try:
            amount = float(amount)
        except (
            ValueError
        ):  # вызывание исключения ValueError если количество валюты не относятся к вещественному типу
            raise APIException(
                f"Не могу перевести количество переводимой валюты, неверно указано число."
            )


class Price:  # создание класса Price для вывода итогового значения
    def __init__(self): ...

    @staticmethod
    def get_price(
        quote, base, amount
    ):  # передача в get_price трех значений отвечающих за ввод пользователя
        base_ticker, quote_ticker = consts.keys[base], consts.keys[quote]
        request = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}"
        )
        # получение данных из сайта creptocompare
        total = str(
            round(
                decimal.Decimal(
                    json.loads(request.content)[base_ticker] * float(amount)
                ),
                8,
            )
        )[::-1]
        
        # 1 получаем информацию из сайта в виде числа
        # 2 умножаем полученое число на введенное пользователем число amount
        # 3 Переводим полученный результат в Decimal формат, что бы избавиться от записей подобного типа 2.643e-05
        # 4 округляем полученное число до 8 знаков после целого значения
        # 5 переводим полученное число в str формат и перевернул его, что бы начать убирать нули в случае
        # если число равно такому формату 0.00043200

        for (
            digit
        ) in (
            total
        ):  # убирание нулей в случае указанном выше, так же в случае если число является целым
            # оно переводится во float а значит надо убрать и точку после 0, тем самым число округлится, если
            # вещественной части нет
            if digit == "0" or digit == ".":
                total = total.replace(digit, "", 1)
            else:
                return total[::-1]
