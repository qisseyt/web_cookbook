# repository.py

import json
import os
from typing import List, Optional
from models import Recipe, Ingredient

class JSONRepository:
    """
    Хранение рецептов (CRUD) в JSON-файле (data/recipes.json).
    Учитываем поле image_url.
    """

    def __init__(self, file_path: str = "data/recipes.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _load_data(self) -> list:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_data(self, data: list):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_all(self) -> List[Recipe]:
        """Возвращает все рецепты как объекты Recipe."""
        data = self._load_data()
        recipes = []
        for item in data:
            ingredients = [Ingredient(**ing) for ing in item["ingredients"]]
            r = Recipe(
                id=item["id"],
                name=item["name"],
                category=item["category"],
                ingredients=ingredients,
                steps=item["steps"],
                image_url=item.get("image_url", "")
            )
            recipes.append(r)
        return recipes

    def get_by_id(self, recipe_id: int) -> Optional[Recipe]:
        for r in self.get_all():
            if r.id == recipe_id:
                return r
        return None

    def save(self, recipe: Recipe) -> Recipe:
        """Создать (если id=0) или обновить (если id!=0) рецепт, затем сохранить JSON."""
        data = self._load_data()
        if recipe.id == 0:
            # Новый
            new_id = 1
            if data:
                existing_ids = [obj["id"] for obj in data]
                new_id = max(existing_ids) + 1
            recipe.id = new_id
            data.append({
                "id": recipe.id,
                "name": recipe.name,
                "category": recipe.category,
                "ingredients": [ing.__dict__ for ing in recipe.ingredients],
                "steps": recipe.steps,
                "image_url": recipe.image_url
            })
        else:
            # Обновление
            updated = False
            for i, obj in enumerate(data):
                if obj["id"] == recipe.id:
                    data[i] = {
                        "id": recipe.id,
                        "name": recipe.name,
                        "category": recipe.category,
                        "ingredients": [ing.__dict__ for ing in recipe.ingredients],
                        "steps": recipe.steps,
                        "image_url": recipe.image_url
                    }
                    updated = True
                    break
            if not updated:
                data.append({
                    "id": recipe.id,
                    "name": recipe.name,
                    "category": recipe.category,
                    "ingredients": [ing.__dict__ for ing in recipe.ingredients],
                    "steps": recipe.steps,
                    "image_url": recipe.image_url
                })
        self._save_data(data)
        return recipe

    def delete(self, recipe_id: int) -> bool:
        data = self._load_data()
        initial_len = len(data)
        data = [obj for obj in data if obj["id"] != recipe_id]
        if len(data) < initial_len:
            self._save_data(data)
            return True
        return False
