import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

class TestOrderCreation:
    def test_create_order_with_auth_and_ingredients(self, create_and_delete_user):
        """Создание заказа с авторизацией и ингредиентами."""
        user = create_and_delete_user
        headers = {"Authorization": user["access_token"], "Content-Type": "application/json"}
        # Получить ингредиенты
        ingredients_response = requests.get(f"{BASE_URL}/ingredients")
        ingredients = ingredients_response.json()["data"][:1]  # Первый ингредиент
        ingredient_ids = [ing["_id"] for ing in ingredients]
        
        response = requests.post(f"{BASE_URL}/orders", headers=headers, json={
            "ingredients": ingredient_ids
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "order" in data

    def test_create_order_without_auth(self):
        """Создание заказа без авторизации."""
        response = requests.post(f"{BASE_URL}/orders", json={
            "ingredients": ["61c0c5a71d1f82001bdaaa6c"]
        })
        assert response.status_code == 401  # Предполагаем, если API требует авторизацию

    def test_create_order_without_ingredients(self, create_and_delete_user):
        """Создание заказа без ингредиентов."""
        user = create_and_delete_user
        headers = {"Authorization": user["access_token"]}
        response = requests.post(f"{BASE_URL}/orders", headers=headers, json={
            "ingredients": []
        })
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Ingredient ids must be provided"

    def test_create_order_invalid_ingredient(self, create_and_delete_user):
        """Создание заказа с неверным хешем ингредиентов."""
        user = create_and_delete_user
        headers = {"Authorization": user["access_token"]}
        response = requests.post(f"{BASE_URL}/orders", headers=headers, json={
            "ingredients": ["invalid_hash"]
        })
        assert response.status_code == 500
