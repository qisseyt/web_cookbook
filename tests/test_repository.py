# tests/test_repository.py
import pytest
from repository import JSONRepository
from models import Recipe

# Тест сохранения рецепта и получения его по ID  
def test_save_and_get_by_id(tmp_path):

    # Создаем временный файл для хранения данных репозитория  
    test_file = tmp_path / "repo_test.json"
    repo = JSONRepository(str(test_file))

    # Создаем объект рецепта и сохраняем его в репозитории 
    r = Recipe(id=0, name="Тест", category="Cat", ingredients=[], steps="", image_url="")
    saved = repo.save(r)

    # Проверяем, что ID сохраненного рецепта равен 1  
    assert saved.id == 1

    # Получаем рецепт по его ID  
    found = repo.get_by_id(1)

    # Проверяем, что рецепт найден и его имя совпадает с исходным
    assert found is not None
    assert found.name == "Тест"

# Тест удаления рецепта из репозитория  
def test_delete(tmp_path):

    # Создаем временный файл для хранения данных репозитория  
    test_file = tmp_path / "repo_test.json"
    repo = JSONRepository(str(test_file))

    # Сохраняем два рецепта в репозитории
    r1 = repo.save(Recipe(0, "A", "Cat", [], "", ""))
    r2 = repo.save(Recipe(0, "B", "Cat", [], "", ""))

    # Проверяем успешное удаление первого рецепта
    assert repo.delete(r1.id) is True

    # Проверяем, что удаленного рецепта больше нет в репозитории 
    assert repo.get_by_id(r1.id) is None

    # Проверяем, что удаление несуществующего рецепта возвращает False  
    assert repo.delete(999) is False
