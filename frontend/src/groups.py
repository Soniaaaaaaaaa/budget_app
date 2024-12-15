import requests


GROUPS_ENDPOINT = "http://localhost:5000" 


def get_group_info(user_id):
    response = requests.get(f"{GROUPS_ENDPOINT}/group", json={'id': user_id})
    if response.status_code == 200:
        return response.json()
    return {}

	
def edit_group(user_id, group_name):
    data = {
        "id": user_id,
        "group_name": group_name
    }
    response = requests.post(f"{GROUPS_ENDPOINT}/group", json=data)
    return response.status_code == 200


def view_members(group_id):
    data = {
        "group_id": group_id,
    }
    response = requests.get(f"{GROUPS_ENDPOINT}/list_members", json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {}


def add_member(group_id, email):
    data = {
        "id": group_id,
        "email": email
    }
    response = requests.post(f"{GROUPS_ENDPOINT}/add_member", json=data)
    return response.status_code == 200


def delete_member(email):
    data = {
        "email": email
    }
    response = requests.post(f"{GROUPS_ENDPOINT}/delete_member", json=data)
    return response.status_code == 200


def create_group(user_id, group_name):
    data = {
        "id": user_id,
        "group_name": group_name
    }
    response = requests.post(f"{GROUPS_ENDPOINT}/create_group", json=data)
    if response.status_code == 200:
        return response.json()['group_id']
    else:
        return None
