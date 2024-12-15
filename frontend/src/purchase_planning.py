import requests


PLANNING_ENDPOINT = 'http://localhost:5004'


def view_shopping_lists(user_id):
    response = requests.get(f"{PLANNING_ENDPOINT}/", json={'user_id': user_id})
        
    if response.status_code == 200:
        return response.json()

    return {}


def view_items(list_id, user_id):
    response = requests.get(f"{PLANNING_ENDPOINT}/view_list", json={'id': list_id, 'user_id': user_id})
        
    if response.status_code == 200:
        return response.json()

    return {}


def add_list(user_id, name, balance):
    data = {
        "user_id": user_id, 
        'name': name, 
        'amount': balance
    }
    response = requests.post(f"{PLANNING_ENDPOINT}/add_new_list", json=data)
    return response.status_code == 200


def add_item(list_id, user_id, name, description, add_info, price):
    data = {
        "list_id": list_id,
        'user_id': user_id,
        'name': name,
        'description': description,
        'add_info': add_info,
        'price': price
    }
    response = requests.post(f"{PLANNING_ENDPOINT}/add_new_item", json=data)
    return response.status_code == 200


def delete_list(list_id, user_id):
    response = requests.post(f"{PLANNING_ENDPOINT}/remove_list", json={'list_id': list_id, 'user_id': user_id})
    return response.status_code == 200


def delete_item(item_id, list_id, user_id):
    data = {
        'list_id': list_id, 
        'user_id': user_id,
        'item_id': item_id
    }
    response = requests.post(f"{PLANNING_ENDPOINT}/remove_item", json=data)
    return response.status_code == 200


def get_propositions(user_id):
    response = requests.get(f"{PLANNING_ENDPOINT}/get_propositions", json={'user_id': user_id})
        
    if response.status_code == 200:
        return response.json()

    return {}
