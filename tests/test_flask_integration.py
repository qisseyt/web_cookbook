import pytest
from app import app

@pytest.fixture
def client():
    """Создаёт тестового клиента Flask"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Тест главной страницы"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Добро пожаловать".encode("utf-8") in response.data  # Проверяем текст на странице

def test_add_recipe(client):
    """Тест API добавления рецепта"""
    response = client.post("/add", json={
        "name": "Салат",
        "category": "Закуски",
        "ingredients": [{"name": "Огурец", "amount": 1, "unit": "шт"}],
        "steps": "Нарезать и перемешать"
    })

    assert response.status_code == 201  # Код успешного создания

def test_get_recipes(client):
    """Тест получения списка рецептов"""
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json, list)
