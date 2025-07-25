"""
Файл класса для базового класса подключения к dvr trassir
Автор: Евгений Петров
Почта: p174@mail.ru
Почта: epoy74@gmail.com
Телефон: +7 952 517 4228
"""

import httpx
from httpx import Response


class TrassirConnector:
    """
    Класс для подключения к видеорегестратору Trassir, производства dssl.
    Используется официальная документация:
    https://www.dssl.ru/files/trassir/manual/ru/setup-sdk.html
    """
    
    _master_login: str | None = None
    _master_password: str | None = None
     

    def __init__(self, host:str, port:int = 8080, timeout: float = 5.0):
        """
        Инициализация экзеппляра класса конкретными значениям:
        host(str): адрес сервера видоеонаблюдения
        port(int): Порт для подключения (по умочанию 8080)
        timeout(float): Таймаут ожидания  при запросе. По умолчанию 5 секунд

        Адрес порта для подключения взят с официального сайта:
        https://www.dssl.ru/files/trassir/manual/ru/sdk-examples-settings.html
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.login: str | None = None
        self.password: str | None = None
        self.sid: str | None = None

    @property
    def master_login(self) -> str | None:
        """
        Возвращает мастер логин, если он объявлен в классе.
        Если мастер логин не задан, возвращает None
        """
        return self._master_login
    
    @master_login.setter
    def master_login(self, dvr_master_login: str) -> str | None:
        """
        Устанавливыает мастер логин для всех регистраторов.

        dvr_master_login(str)  - мастер логин для регистраторов

        return: Если все корректно, возвращает присвоенный логин
        """
        if isinstance(dvr_master_login, str):
            self._master_login = dvr_master_login
            return self._master_login
        else:
            err = (
                f"Мастер логин должен быть строкой, "
                f"текущий тип логина: {type(dvr_master_login)}"
                )
            raise ValueError(err)
        
    @property
    def master_password(self) -> str | None:
        """
        Возвращает мастер пароль, если он объявлен в классе.
        Если мастер пароль не объявлен, возвращает None
        """
        return self._master_password
    
    @master_password.setter
    def master_password(self, dvr_master_password: str) -> str | None:
        """
        Устанавливыает мастер пароль для всех регистраторов.

        dvr_master_login(str)  - мастер пароль для регистраторов

        return: Если все корректно, возвращает присвоенный логин
        """
        if isinstance(dvr_master_password, str):
            self._master_password = dvr_master_password
            return self._master_password
        else:
            err = (
                f"Мастер пароль должен быть строкой, "
                f"текущий тип логина: {type(dvr_master_password)}"
                )
            raise ValueError(err)
    
    def identification(
            self, 
            dvr_login: str = "",
            dvr_password: str = "") -> bool:
        """
        Автоизация на сервере видеонаблюдения.
        Официальная информация:
        https://www.dssl.ru/files/trassir/manual/ru/sdk-examples-id.html
        Пример запроса:
        https://192.168.1.200:8080/login?username=Admin&password=987654321

        login(str): Логин для идентификации По умолчанию: ""
        password(str): Пароль для идентификации. По умолчанию: ""
        """
        self.login = dvr_login
        self.password = dvr_password

        ENDPOINT = f"https://{self.host}:{self.port}/login?username={self.login}&password={self.password}"

        try:
            responce: Response = httpx.post(ENDPOINT)
        except Exception as err:
            raise err

        try:
            if responce.status_code == 200:
                self.sid = responce.json()["sid"]
                print(f"Сервер: {self.host}, sid: {self.sid}")
                return True
            else:
                return False
        except Exception as err:
            raise err
    
