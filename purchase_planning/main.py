from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL
from config import Config
from models.user import User
from models.group import Group
from models.purchase_plan import PurchasePlan
from models.item import Item, ItemBlueprint
import os
import requests

# CURR_MSG = ""

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

# MSG_ADD_ITEM = {
# 	0: "Something went wrong!",
# 	2: "Cound not find shopping list!",
# 	3: "You do not belong to this family!",
# 	4: "Price exceeds balance of the list!"
# }

# MSG_REMOVE_ITEM = {
# 	0: "Something went wrong!",
# 	2: "Cound not find shopping list!",
# 	3: "You do not belong to this family!"
# }

# user = None
# shopping_lists = None

def get_cursor():
	connection = mysql.connection
	cursor = connection.cursor()
	return connection, cursor

# def define_user():
# 	global user, shopping_lists
# 	user = User.get_user_by_id(get_cursor()[1], 1)
# 	shopping_lists = PurchasePlan.get_purchase_plans_by_group(get_cursor()[1], user.group)

@app.route("/", methods=["GET", "POST"])
def index():
	data = request.json
	user_id = data["user_id"]
	user = User.get_user_by_id(get_cursor()[1], user_id)
	shopping_lists: list[PurchasePlan] = PurchasePlan.get_purchase_plans_by_group(get_cursor()[1], user.group)
	result = [{
		'list_id': shopping_list.id, 'name': shopping_list.name,
		'balance': shopping_list.balance
	} for shopping_list in shopping_lists]
	return result

# @app.route("/list_form", methods=["GET", "POST"])
# def new_list_form():
# 	return render_template('new_list.html')

@app.route("/get_propositions", methods=["GET", "POST"])
def new_item_form():
	data = request.json
	user_id = data['user_id']
	user = User.get_user_by_id(get_cursor()[1], user_id)
	propositions: list[str] = Group.get_propositions(get_cursor()[1], user.group.id)
	result = [{'text': proposition} for proposition in propositions]
	return result

@app.route("/add_new_list", methods=["GET", "POST"])
def add_new_list():
	data = request.json
	name = data['name']
	balance = data['amount']
	user_id = data['user_id']
	user = User.get_user_by_id(get_cursor()[1], user_id)
	connection, cursor = get_cursor()
	status = PurchasePlan.add_purchase_plan(cursor, connection, name, user.group, balance)
	return {'status': status}

@app.route("/add_new_item", methods=["GET", "POST"])
def add_new_item():
	connection, cursor = get_cursor()
	data = request.json
	name = data['name']
	description = data['description']
	add_info = data['add_info']
	price = data['price']
	list_id = data['list_id']
	user_id = data['user_id']
	user = User.get_user_by_id(get_cursor()[1], user_id)
	shopping_list = PurchasePlan.get_purchase_plan_by_id(get_cursor()[1], user.group, list_id)
	if shopping_list is None:
		return None
	code = shopping_list.add_item(cursor, connection, name, description, add_info, price, user)
	return {'status': code}

@app.route("/view_list", methods=["GET", "POST"])
def view_list():
	data = request.json
	list_id = data['id']
	user_id = data['user_id']
	user = User.get_user_by_id(get_cursor()[1], user_id)
	shopping_list = PurchasePlan.get_purchase_plan_by_id(get_cursor()[1], user.group, list_id)
	if shopping_list is None:
		return None
	result = [{
		'item_id': item.id, 'name': item.item_blueprint.name,
		'description': item.item_blueprint.description,
		'info': item.additional_info, 'price': item.price
	} for item in shopping_list.items]
	return result

@app.route("/remove_item", methods=["GET", "POST"])
def remove_item():
	connection, cursor = get_cursor()
	data = request.json
	list_id = data['list_id']
	item_id = data['item_id']
	user_id = data['user_id']
	user = User.get_user_by_id(get_cursor()[1], user_id)
	shopping_list = PurchasePlan.get_purchase_plan_by_id(get_cursor()[1], user.group, list_id)
	if shopping_list is None:
		return None
	for item in shopping_list.items:
		if item.id == item_id:
			shopping_list: PurchasePlan
			code = shopping_list.remove_item(cursor, connection, item.id, user)
			return {'status': code}
	return {'status': 4}

@app.route("/remove_list", methods=["GET", "POST"])
def remove_list():
	data = request.json
	list_id = data['list_id']
	user_id = data['user_id']
	user = User.get_user_by_id(get_cursor()[1], user_id)
	connection, cursor = get_cursor()
	if PurchasePlan.check_user_plan(cursor, user.id, list_id):
		status = PurchasePlan.delete_purchase_plan(cursor, connection, list_id)
		return {'status': status}
	else:
		return None


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5004)