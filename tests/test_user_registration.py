import pytest
import requests
import uuid

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

class TestUserRegistration:
    def test_create_unique_user(self):
        """Создание уникального пользователя."""
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

    def test_create_existing_user(self):
        """Создание пользователя, который уже зарегистрирован."""
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

    def test_create_user_missing_field(self):
        """Создание пользователя без обязательного поля (email)."""
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "password": "password",
            "name": "MissingEmail"
        })
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"
