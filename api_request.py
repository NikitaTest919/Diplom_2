import requests
import allure

@allure.step("Создание нового пользователя")
def create_user(base_url, email, password, name):
    response = requests.post(f"{base_url}/auth/register", json={
        "email": email,
        "password": password,
        "name": name
    })
    return response

@allure.step("Удаление пользователя")
def delete_user(base_url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(f"{base_url}/auth/user", headers=headers)
    return response
