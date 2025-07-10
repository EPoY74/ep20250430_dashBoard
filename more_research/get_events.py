"""
Скрипт с https://www.dssl.ru/files/trassir/manual/ru/sdk-python.html
Переделаный на Пайтон 3 и доработанный.
Для проверки работы sdk
"""

import logging
import os
import time

import aiohttp
import dotenv
import requests


def init_logger():
    """
    Инициализирует логгер для дальнейшей работы
    """

    logging.basicConfig(
        level=logging.DEBUG,  # Уровень логгирования
        format="%(asctime)s - %(levelname)s - %(message)s",  # формат
        # если хочешь писать в файл
        # filename='app.log',
        # 'a' — добавлять, 'w' — перезаписывать
        # filemode='a'
    ) # задержка между запросами


init_logger()

dotenv.load_dotenv()

LOGIN_URL = str(os.getenv("LOGIN_URL"))
EVENTS_URL = str(os.getenv("EVENTS_URL"))
DVR_USER_NAME = os.getenv("DVR_USER_NAME")
if DVR_USER_NAME is None:
    print_to_user = (
        "Переменная окружения не найдена. "
        "Задайте переменную окружения DVR_USER_NAME"
    )
    logging.error(print_to_user)
    exit(print_to_user)
elif DVR_USER_NAME == "":
    print_to_user = (
        "Переменная океружения DVR_USER_NAME пустая. "
        "Задайте значение для данной переменной"
    )
    logging.error(print_to_user)
    exit(print_to_user)
DVR_PASSWORD = os.getenv("DVR_PASSWORD")


def main():
    """
    Точка входа в скрипт
    """



    # Авторизация
    resp = requests.get(
        LOGIN_URL,
        params={"username": DVR_USER_NAME, "password": DVR_PASSWORD},
        verify=False,
        timeout=5,
    )
    logging.debug("Login response code: %s", resp.status_code)
    logging.debug("Login response body: %s", resp.text)
    input()

    sid = resp.json().get("sid")
    logging.debug("My session: %s", sid)


    # Получение событий
    while True:
        try:
            r = requests.get(
                EVENTS_URL,
                params={"sid": sid},
                verify=False,
                timeout=5,
            )
            logging.info(r.text)
        except Exception as e:
            logging.error("Error: %s", str(e))
            raise
        input()
        time.sleep(1) 



if __name__ ==  "__main__":
    main()