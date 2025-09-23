import pytest
import requests
import allure
from urls import BASE_URL

class TestUserLogin:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, create_and_delete_user):
        user = create_and_delete_user
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data

    @allure.title("Логин с неверным логином и паролем")
    def test_login_invalid_credentials(self):
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "invalid@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "email or password are incorrect"
