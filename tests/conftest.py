import pytest
import uuid
from urls import BASE_URL
from data import create_user, delete_user

@pytest.fixture(scope="function")
def create_and_delete_user():
    """Фикстура для создания уникального пользователя перед тестом и удаления после."""
    email = f"test-{uuid.uuid4()}@yandex.ru"
    password = "password"
    name = "TestUser"
    
    response = create_user(BASE_URL, email, password, name)
    if response.status_code != 200:
        pytest.skip("Не удалось создать тестового пользователя")
    user_data = response.json()
    access_token = user_data.get("accessToken")
    
    yield {"email": email, "password": password, "name": name, "access_token": access_token}
    
    # Удаляем пользователя после теста
    if access_token:
        delete_response = delete_user(BASE_URL, access_token)
        if delete_response.status_code != 202:
            print(f"Warning: не удалось удалить пользователя: {delete_response.status_code} {delete_response.text}")
