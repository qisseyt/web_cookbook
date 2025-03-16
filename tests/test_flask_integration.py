from app import app
import pytest

# Фикстура pytest для создания тестового клиента Flask.

@pytest.fixture
def client():
    # Включаем тестовый режим приложения  
    app.config["TESTING"] = True

    # Создаем тестовый клиент и передаем его в тесты  
    with app.test_client() as c:
        yield c

# Тест главной страницы ("/")  

def test_index_page(client):
    # Отправляем GET-запрос на главную страницу
    resp = client.get("/")

    # Проверяем, что сервер отвечает статусом 200 (OK)
    assert resp.status_code == 200

    # Проверяем, что в ответе содержится строка "Список рецептов", закодированная в UTF-8 
    assert "Список рецептов".encode("utf-8") in resp.data

    # Проверяем
    assert "То чего точно нет".encode("utf-8") in resp.data
