# models.py
from dataclasses import dataclass
from typing import List

@dataclass
class Ingredient:
    """Описывает один ингредиент."""
    name: str
    amount: float
    unit: str

@dataclass
class Recipe:
    """
    Описывает рецепт (с ингредиентами, опциональной картинкой).
    image_url - "/static/uploads/..." или "" (если нет картинки).
    """
    id: int
    name: str
    category: str
    ingredients: List[Ingredient]
    steps: str
    image_url: str
