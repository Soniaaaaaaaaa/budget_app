from flask import Flask, request
from flask_mysqldb import MySQL
from config import Config
from models.budget import Budget
from models.category import Category
from models.expense import Expense
import json
import pika


app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'budget_notifications'


# def send_to_queue(message):
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
#     channel = connection.channel()
#     channel.queue_declare(queue=QUEUE_NAME, durable=True)
#     channel.basic_publish(
#         exchange='',
#         routing_key=QUEUE_NAME,
#         body=message,
#         properties=pika.BasicProperties(delivery_mode=2) 
#     )
#     connection.close()
 

def get_cursor():
    return mysql.connection.cursor()


@app.route('/')
def redirect_to_budgets():
    return 'budget management service'


@app.route('/all_budgets/<int:group_id>')
def all_budgets(group_id):
    cursor = get_cursor()
    budgets = Budget.get_all_budgets_by_group(cursor, group_id)
    result = {
        "budgets": budgets
    }
    return result


@app.route('/add_budget', methods=['POST'])
def add_budget():
    if request.method == 'POST':
        data = request.json
        group_id = data['group_id']
        budget_name = data['budget_name']
        total_budget = data['total_budget']
        cursor = get_cursor()

        Budget.add_budget(cursor, group_id, budget_name, total_budget)
        mysql.connection.commit()

        # message = {
        #     'notification': 'add_budget',
        #     'group_id': group_id
        # }
        # send_to_queue(message)

        return {"status": "success"}


@app.route('/update_budget/<int:budget_id>', methods=['POST'])
def update_budget(budget_id):
    if request.method == 'POST':
        data = request.json
        budget_name = data['budget_name']
        total_budget = data['total_budget']
        cursor = get_cursor()

        Budget.update_budget(cursor, budget_id, budget_name, total_budget)
        mysql.connection.commit()

        return {"status": "success"}


@app.route('/delete_budget/<int:budget_id>')
def delete_budget(budget_id):
    cursor = get_cursor()
    Budget.delete_budget(cursor, budget_id)
    mysql.connection.commit()

    return {"status": "success"}


@app.route('/expenses/<int:budget_id>')
def view_expenses(budget_id):
    cursor = get_cursor()
    budget = Budget.get_budget_name_by_id(cursor, budget_id)
    expenses = Expense.get_all_expenses_by_budget(cursor, budget_id)
    spent_this_month = Expense.sum_current_expenses_this_month(cursor, budget_id)
    categories = Category.get_all_categories(cursor)

    result = {
        'budget': budget,
        'expenses': expenses,
        'spent_this_month': spent_this_month,
        'categories': categories
    }
 
    return result


@app.route('/add_expense', methods=['POST'])
def add_expense():
    if request.method == 'POST':
        data = request.json
        budget_id = data['budget_id']
        description = data['description']
        price = data['price']
        expense_type = data['expense_type']
        category_id = data['category_id']
        cursor = get_cursor()

        Expense.add_expense(cursor, budget_id, description, price, expense_type, category_id)
        mysql.connection.commit()

        return {"status": "success"}


@app.route('/delete_expense/<int:expense_id>', methods=['GET'])
def delete_expense(expense_id):
    cursor = get_cursor()
    Expense.delete_expense(cursor, expense_id)
    mysql.connection.commit()

    return {"status": "success"}


@app.route('/update_expense/<int:expense_id>', methods=['POST'])
def update_expense(expense_id):
    if request.method == 'POST':
        data = request.json
        description = data['description']
        price = data['price']
        expense_type = data['expense_type']
        category_id = data['category_id']
        cursor = get_cursor()

        Expense.update_expense(cursor, expense_id, description, price, expense_type, category_id)
        mysql.connection.commit()

        return {"status": "success"}
        

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5001)
     