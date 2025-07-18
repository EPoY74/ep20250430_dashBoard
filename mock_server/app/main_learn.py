"""
Исследователькой программирование: Пишу моковый сервер для
тестирования дашбоарда дла dar trassir
"""

from fastapi import FastAPI

from mock_server.app.models_learn import Item

app = FastAPI()


@app.get("/")
def read_root():
    """
    Основной обработчик
    """
    return {"message": "Hello fastapi"}


@app.get("/hello")
def say_hello(name: str = "Гость"):
    """
    Приветствует гостя.

    Аргуметнты:
    name(str): Имя гостя, которого приветсвуем
    """
    return {"message": f"Привет, {name}!"}


@app.get("/item/{item_id}")
def read_item(item_id: int, detail: bool | None = False):
    """
    Возвращает информацию об одном объекте с номером item_id

    Аргументы:
    item_id(int): номер объекта
    """
    return {"item_id": item_id, "detail": detail}


@app.post("/items/")
def create_item(item: Item):
    """
    Создаю объект
    """
    return {"message": f"Товар {item.name} создан!", "data": item}
