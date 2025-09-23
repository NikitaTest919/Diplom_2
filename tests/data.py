# data.py
import requests

def create_user(base_url, email, password, name):
    response = requests.post(f"{base_url}/auth/register", json={
        "email": email,
        "password": password,
        "name": name
    })
    return response

def delete_user(base_url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(f"{base_url}/auth/user", headers=headers)
    return response
