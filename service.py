# service.py

from typing import List
from copy import deepcopy
from models import Recipe, Ingredient
from repository import JSONRepository

class RecipeService:
    """
    Бизнес-логика: создание, редактирование, удаление, поиск,
    временное масштабирование.
    """

    def __init__(self, repository: JSONRepository):
        self.repository = repository

    def add_recipe(self, name: str, category: str,
                   ingredients_data: List[dict],
                   steps: str, image_url: str = "") -> Recipe:
        ings = [Ingredient(**ing) for ing in ingredients_data]
        new_recipe = Recipe(
            id=0,
            name=name,
            category=category,
            ingredients=ings,
            steps=steps,
            image_url=image_url
        )
        return self.repository.save(new_recipe)

    def edit_recipe(self, recipe_id: int, name: str, category: str,
                    ingredients_data: List[dict], steps: str,
                    new_image_url: str = None) -> Recipe:
        existing = self.repository.get_by_id(recipe_id)
        if not existing:
            raise ValueError(f"Рецепт с ID {recipe_id} не найден.")

        existing.name = name
        existing.category = category
        existing.ingredients = [Ingredient(**ing) for ing in ingredients_data]
        existing.steps = steps

        if new_image_url is not None:
            existing.image_url = new_image_url

        return self.repository.save(existing)

    def delete_recipe(self, recipe_id: int) -> bool:
        return self.repository.delete(recipe_id)

    def get_all_recipes(self) -> List[Recipe]:
        return self.repository.get_all()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        r = self.repository.get_by_id(recipe_id)
        if not r:
            raise ValueError(f"Рецепт с ID {recipe_id} не найден.")
        return r

    def find_by_name(self, query: str) -> List[Recipe]:
        q_lower = query.lower()
        return [r for r in self.get_all_recipes() if q_lower in r.name.lower()]

    def find_by_ingredient(self, query: str) -> List[Recipe]:
        q_lower = query.lower()
        matched = []
        for r in self.get_all_recipes():
            for ing in r.ingredients:
                if q_lower in ing.name.lower():
                    matched.append(r)
                    break
        return matched

    def filter_by_category(self, category: str) -> List[Recipe]:
        cat_lower = category.lower()
        return [r for r in self.get_all_recipes() if r.category.lower() == cat_lower]

    def scale_recipe_temporarily(self, recipe_id: int, factor: float) -> Recipe:
        """Возвращает КОПИЮ рецепта с умноженными ингредиентами, не сохраняя в JSON."""
        original = self.get_recipe_by_id(recipe_id)
        scaled = deepcopy(original)
        for ing in scaled.ingredients:
            ing.amount *= factor
        return scaled
