import pytest
import requests
import allure
from urls import BASE_URL

class TestOrderRetrieval:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self, create_and_delete_user):
        user = create_and_delete_user
        headers = {"Authorization": user["access_token"]}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "orders" in data  # Предполагаем структуру

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"
