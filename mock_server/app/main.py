"""
Исследователькой программирование: Пишу моковый сервер для 
тестирования дашбоарда дла dar trassir
"""

import models
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    '''
    Основной обработчик
    '''
    return{"message": "Hello fastapi"}

@app.get("/hello")
def say_hello(name: str = "Гость"):
    """
    Приветствует гостя.

    Аргуметнты: 
    name(str): Имя гостя, которого приветсвуем
    """
    return {"message": f"Привет, {name}!"}
