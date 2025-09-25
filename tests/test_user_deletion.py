import pytest
import requests
import allure
from Diplom_2.urls import BASE_URL
from Diplom_2.api_request import delete_user

class TestUserDeletion:
    @allure.title("Удаление пользователя с авторизацией должно проходить успешно")
    def test_delete_user_with_auth(self, create_and_delete_user):
        user = create_and_delete_user
        token = user["access_token"]
        response = delete_user(BASE_URL, token)
        assert response.status_code == 202 or response.status_code == 200
        data = response.json()
        assert data.get("success") is True

        # Попытка получить данные пользователя после удаления - ожидаем ошибку (например, 401 или 404)
        headers = {"Authorization": f"Bearer {token}"}
        get_response = requests.get(f"{BASE_URL}/auth/user", headers=headers)
        assert get_response.status_code in (401, 404)

    @allure.title("Удаление пользователя без авторизации должно быть запрещено")
    def test_delete_user_without_auth(self):
        response = requests.delete(f"{BASE_URL}/auth/user")
        assert response.status_code == 401
        data = response.json()
        assert data.get("success") is False
        assert "You should be authorised" in data.get("message", "")

    @allure.title("Удаление пользователя с некорректным токеном должно быть запрещено")
    def test_delete_user_with_invalid_token(self):
        headers = {"Authorization": "Bearer invalidtoken123"}
        response = requests.delete(f"{BASE_URL}/auth/user", headers=headers)
        assert response.status_code == 401 or response.status_code == 403
        data = response.json()
        assert data.get("success") is False
