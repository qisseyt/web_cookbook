import pytest
from repository import JSONRepository
from models import Recipe

@pytest.fixture
def repo(tmp_path):
    """Создаёт временный JSON-файл для тестового репозитория"""
    test_file = tmp_path / "test_recipes.json"
    return JSONRepository(file_path=str(test_file))

def test_save_and_get_recipe(repo):
    """Тест сохранения и получения рецепта"""
    recipe = Recipe(id=1, name="Пицца", category="Ужин", ingredients=[], steps="Готовим тесто...")
    repo.save(recipe)

    retrieved_recipe = repo.get_by_id(1)

    assert retrieved_recipe is not None
    assert retrieved_recipe.name == "Пицца"

def test_get_all(repo):
    """Тест получения всех рецептов"""
    repo.save(Recipe(id=1, name="Омлет", category="Завтрак", ingredients=[], steps=""))
    repo.save(Recipe(id=2, name="Борщ", category="Суп", ingredients=[], steps=""))

    recipes = repo.get_all()

    assert len(recipes) == 2
    assert {r.id for r in recipes} == {1, 2}

def test_delete_recipe(repo):
    """Тест удаления рецепта"""
    repo.save(Recipe(id=1, name="Паста", category="Ужин", ingredients=[], steps=""))
    
    assert repo.delete(1) is True
    assert repo.get_by_id(1) is None
