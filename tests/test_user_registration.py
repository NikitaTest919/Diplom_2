import pytest
import requests
import uuid
import allure
from Diplom_2.urls import BASE_URL

class TestUserRegistration:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        email = f"unique-{uuid.uuid4()}@yandex.ru"
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": "password",
            "name": "UniqueUser"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data
        # Удаление после (если нужно, вызовите фикстуру или API)

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        email = "existing@test.com"  # Предполагаем существующий
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": "password",
            "name": "ExistingUser"
        })
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля (email)")
    def test_create_user_missing_field(self):
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "password": "password",
            "name": "MissingEmail"
        })
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"
