"""
Скрипт с https://www.dssl.ru/files/trassir/manual/ru/sdk-python.html
Переделаный на Пайтон 3 и доработанный.
Для проверки работы sdk
"""

import logging
import time

import aiohttp
import dotenv
import requests

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логгирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # формат
    
    # если хочешь писать в файл
    # filename='app.log',
    
    # 'a' — добавлять, 'w' — перезаписывать
    # filemode='a'
)


dotenv.load_dotenv()

LOGIN_URL = "https://10.1.15.100:8080/login"
EVENTS_URL = "https://10.1.15.100:8080/health"

# Авторизация
resp = requests.get(
    LOGIN_URL,
    params={"username": "admin", "password": "7905520Tr"},
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
    time.sleep(1)  # задержка между запросами
