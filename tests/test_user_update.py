import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

class TestUserUpdate:
    def test_update_user_with_auth(self, create_and_delete_user):
        """Изменение данных с авторизацией (email)."""
        user = create_and_delete_user
        headers = {"Authorization": user["access_token"]}
        response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json={
            "email": f"updated-{user['email']}"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["email"] == f"updated-{user['email']}"

    def test_update_user_without_auth(self):
        """Изменение данных без авторизации."""
        response = requests.patch(f"{BASE_URL}/auth/user", json={
            "email": "noauth@test.com"
        })
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"

    # Аналогично для name и других полей
    def test_update_user_existing_email(self, create_and_delete_user):
        """Изменение на существующий email."""
        user = create_and_delete_user
        headers = {"Authorization": user["access_token"]}
        response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json={
            "email": "existing@test.com"
        })
        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "User with such email already exists"
