import pytest
import requests
import uuid  # Для генерации уникальных email

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

@pytest.fixture(scope="function")
def create_and_delete_user():
    """Фикстура для создания уникального пользователя перед тестом и удаления после."""
    email = f"test-{uuid.uuid4()}@yandex.ru"
    password = "password"
    name = "TestUser"
    
    # Создание пользователя
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": password,
        "name": name
    })
    assert response.status_code == 200, "Не удалось создать тестового пользователя"
    user_data = response.json()
    access_token = user_data["accessToken"]
    
    yield {"email": email, "password": password, "name": name, "access_token": access_token}
    
    # Удаление пользователя (если есть эндпоинт для удаления; иначе пропустить)
    # Предполагаем, что API не имеет удаления, но фикстура готова для расширения
    # Если удаление нужно, добавьте код здесь
