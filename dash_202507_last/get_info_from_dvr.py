"""
Файл для  подключения к dvr trassir
Автор: Евгений Петров
Почта: p174@mail.ru
Почта: epoy74@gmail.com
Телефон: +7 952 517 4228
"""

from dvr_lib import TrassirConnector

tr15 = TrassirConnector("10.1.15.115")

try:
    if tr15.identification("p174@mail.ru", "_EPoY_1980_"):
        print("Подключение к серверу успешно") #noqa
    else:
        print("подключение к серверу не удалось") #noqa
except Exception as err:
    raise err
