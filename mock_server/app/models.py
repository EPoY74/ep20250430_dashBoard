"""
Модели для использования валидации данных
"""


from pydantic import BaseModel


class Item(BaseModel):
    """
    Класс для создания единицы товара
    """
    name: str
    description: str | None = None
    price: float = 0
    in_stock: True = True
