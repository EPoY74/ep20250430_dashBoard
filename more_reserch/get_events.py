"""
Скрипт с https://www.dssl.ru/files/trassir/manual/ru/sdk-python.html
Переделаный на Пайтон 3 и доработанный.
Для проверки работы sdk
"""

import logging
import time

import dotenv
import requests

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логгирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # формат
    # filename='app.log',                      # если хочешь писать в файл
    # filemode='a'                             # 'a' — добавлять, 'w' — перезаписывать
)


dotenv.load_dotenv()

login_url = "https://10.1.15.100:8080/login"
events_url = "https://10.1.15.100:8080/health"

# Авторизация
resp = requests.get(
    login_url,
    params={"username": "****", "password": "****"},
    verify=False,
)
logging.debug("Login response code: %s", resp.status_code)
logging.debug("Login response body: %s", resp.text)
input()

sid = resp.json().get("sid")
logging.debug(f"My session: {sid}")


# Получение событий
while True:
    try:
        r = requests.get(events_url, params={"sid": sid}, verify=False)
        logging.info(r.text)
    except Exception as e:
        logging.error("Error:", e)
        raise
    input()
    time.sleep(1)  # задержка между запросами
