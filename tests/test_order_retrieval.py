import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

class TestOrderRetrieval:
    def test_get_orders_authorized(self, create_and_delete_user):
        """Получение заказов авторизованного пользователя."""
        user = create_and_delete_user
        headers = {"Authorization": user["access_token"]}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "orders" in data  # Предполагаем структуру

    def test_get_orders_unauthorized(self):
        """Получение заказов неавторизованного пользователя."""
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"
