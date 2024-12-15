import requests


BUDGETS_ENDPOINT = "http://localhost:5001" 


def get_all_budgets(group_id):
    response = requests.get(f"{BUDGETS_ENDPOINT}/all_budgets/{group_id}")
    if response.status_code == 200:
        return response.json()
    return {}


def add_budget(group_id, budget_name, total_budget):
    data = {
        "group_id": group_id,
        "budget_name": budget_name,
        "total_budget": total_budget
    }
    response = requests.post(f"{BUDGETS_ENDPOINT}/add_budget", json=data)
    return response.status_code == 200


def delete_budget(budget_id):
    response = requests.get(f"{BUDGETS_ENDPOINT}/delete_budget/{budget_id}")
    return response.status_code == 200


def edit_budget(budget_id, budget_name, total_budget):
    data = {
        "budget_name": budget_name,
        "total_budget": total_budget
    }
    response = requests.post(f"{BUDGETS_ENDPOINT}/update_budget/{budget_id}", json=data)
    return response.status_code == 200


def get_expenses(budget_id):
    response = requests.get(f"{BUDGETS_ENDPOINT}/expenses/{budget_id}")
    if response.status_code == 200:
        return response.json()
    return {}


def add_expense(budget_id, description, price, expense_type, category_id):
    data = {
        'budget_id': budget_id, 
        'description': description, 
        'price': price, 
        'expense_type': expense_type, 
        'category_id': category_id
    }
    response = requests.post(f"{BUDGETS_ENDPOINT}/add_expense", json=data)
    return response.status_code == 200


def delete_expense(expense_id):
    response = requests.get(f"{BUDGETS_ENDPOINT}/delete_expense/{expense_id}")
    return response.status_code == 200


def edit_expense(expense_id, description, price, expense_type, category_id):
    data = {
        "description": description,
        "price": price,
        'expense_type': expense_type, 
        'category_id': category_id
    }
    response = requests.post(f"{BUDGETS_ENDPOINT}/update_expense/{expense_id}", json=data)
    return response.status_code == 200