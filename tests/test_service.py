import pytest
from service import RecipeService
from repository import JSONRepository
from models import Recipe, Ingredient

@pytest.fixture
def service(tmp_path):
    """Создаёт временный JSON-файл для тестового репозитория"""
    test_file = tmp_path / "test_recipes.json"
    repo = JSONRepository(file_path=str(test_file))
    return RecipeService(repo)

def test_add_recipe(service):
    """Тест добавления нового рецепта"""
    ing_data = [{"name": "Мука", "amount": 200, "unit": "г"}]

    recipe = service.add_recipe("Пирог", "Десерт", ing_data, "Шаги...")

    assert recipe.id == 1
    assert recipe.name == "Пирог"
    assert recipe.category == "Десерт"
    assert len(recipe.ingredients) == 1

def test_find_by_name(service):
    """Тест поиска рецепта по имени"""
    service.add_recipe("Омлет", "Завтрак", [], "")
    service.add_recipe("Пицца", "Ужин", [], "")

    result = service.find_by_name("Омлет")

    assert result is not None
    assert result.name == "Омлет"

def test_filter_by_category(service):
    """Тест фильтрации по категории"""
    service.add_recipe("Окрошка", "Суп", [], "")
    service.add_recipe("Борщ", "Суп", [], "")
    service.add_recipe("Торт", "Десерт", [], "")

    result = service.filter_by_category("Суп")

    assert len(result) == 2
    assert all(recipe.category == "Суп" for recipe in result)

def test_delete_recipe(service):
    """Тест удаления рецепта"""
    recipe = service.add_recipe("Блины", "Завтрак", [], "")
    assert service.delete_recipe(recipe.id) is True

    assert service.find_by_name("Блины") is None
