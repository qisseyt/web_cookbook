# tests/test_service.py
import pytest
from service import RecipeService
from repository import JSONRepository
from models import Recipe, Ingredient

@pytest.fixture
def service(tmp_path):
    """
    Создаем временный JSON-файл (test_recipes.json) в папке tmp_path.
    Возвращаем экземпляр RecipeService, где repository указывает на этот файл.
    """
    test_file = tmp_path / "test_recipes.json"
    repo = JSONRepository(file_path=str(test_file))
    return RecipeService(repo)

def test_add_recipe(service):
    # Arrange
    ings = [{"name": "Мука", "amount": 200, "unit": "г"}]
    # Act
    recipe = service.add_recipe("Пирог", "Десерт", ings, "Шаги...")
    # Assert
    assert recipe.id == 1
    assert recipe.name == "Пирог"
    assert len(recipe.ingredients) == 1

def test_edit_recipe_not_found(service):
    # Пытаемся отредактировать несуществующий рецепт.
    with pytest.raises(ValueError):
        service.edit_recipe(
            999,  # Нет такого ID
            name="New name", 
            category="New cat",
            ingredients_data=[],
            steps="New steps"
        )

def test_filter_by_category(service):
    # Arrange
    service.add_recipe("Окрошка", "Суп", [], "")
    service.add_recipe("Борщ", "Суп", [], "")
    service.add_recipe("Торт", "Десерт", [], "")

    # Act
    result = service.filter_by_category("Суп")

    # Assert
    assert len(result) == 2