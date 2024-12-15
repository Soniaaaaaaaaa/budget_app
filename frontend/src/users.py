import requests


USERS_ENDPOINT = "http://localhost:5000" 


def user_login(email, password):
    data = {
        "email": email,
        "password": password,
    }
    response = requests.get(f"{USERS_ENDPOINT}/login", json=data)
    if response.status_code == 200:
        return response.json()
    else: 
        return False


def user_register(email, password):
    data = {
        "email": email,
        "password": password,
    }
    response = requests.post(f"{USERS_ENDPOINT}/register", json=data)
    return response.status_code == 200


def get_user_info(user_id):
    response = requests.get(f"{USERS_ENDPOINT}/profile", json={'id': user_id})
    if response.status_code == 200:
        return response.json()
    return {}


def edit_user(user_id, username, old_password, new_password):
    data = {
        "id": user_id,
        "username": username,
        "current_password": old_password,
        "new_password": new_password
    }
    response = requests.post(f"{USERS_ENDPOINT}/profile", json=data)
    return response.status_code == 200


def validate_token(token):
    data = {
        'token': token
    }

    response = requests.post(f"{USERS_ENDPOINT}/validate", json=data)
    return response.status_code == 200
