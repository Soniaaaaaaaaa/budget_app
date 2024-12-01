from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL
from config import Config
from models.user import User
from models.group import Group
from models.purchase_plan import PurchasePlan
from models.item import Item, ItemBlueprint
import os

CURR_MSG = ""

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

MSG_ADD_ITEM = {
	0: "Something went wrong!",
	2: "This item is already in shopping list!",
	3: "You do not belong to this family!",
	4: "Price exceeds balance of the list!"
}

MSG_REMOVE_ITEM = {
	0: "Something went wrong!",
	2: "This item is not found in shopping list!",
	3: "You do not belong to this family!"
}

user = None
shopping_lists = None

def get_cursor():
	connection = mysql.connection
	cursor = connection.cursor()
	return connection, cursor

def define_user():
	global user, shopping_lists
	user = User.get_user_by_id(get_cursor()[1], 1)
	shopping_lists = PurchasePlan.get_purchase_plans_by_group(get_cursor()[1], user.group)

@app.route("/")
def index():
	global CURR_MSG
	msg = CURR_MSG
	CURR_MSG = ""
	define_user()
	return render_template(
		'index.html', user_name=user.name, group_name=user.group.name,
		lists=shopping_lists, has_lists=len(shopping_lists) > 0,
		has_massage=len(msg) > 0, msg=msg
	)

@app.route("/list_form")
def new_list_form():
	return render_template('new_list.html')

@app.route("/item_form")
def new_item_form():
	list_id = request.args.get('list_id')
	return render_template('new_item.html', list_id=list_id)

@app.route("/add_new_list")
def add_new_list():
	global CURR_GROUP_ID
	global shopping_lists
	name = request.args.get('name')
	balance = float(request.args.get('amount'))
	connection, cursor = get_cursor()
	PurchasePlan.add_purchase_plan(cursor, connection, name, user.group, balance)
	return redirect('/')

@app.route("/add_new_item")
def add_new_item():
	global CURR_MSG
	connection, cursor = get_cursor()
	name = request.args.get('name')
	description = request.args.get('description')
	add_info = request.args.get('add_info')
	price = float(request.args.get('price'))
	list_id = int(request.args.get('list_id'))
	for shopping_list in shopping_lists:
		if shopping_list.id == list_id:
			code = shopping_list.add_item(cursor, connection, name, description, add_info, price, user)
			if code != 1:
				global CURR_MSG
				CURR_MSG = f"We could not add item to the shopping list: {MSG_ADD_ITEM[code]}"
			return redirect(f'/view_list?id={shopping_list.id}')
	CURR_MSG = "For some reason, we could not find the shopping list you specified!"
	return redirect('/')

@app.route("/view_list")
def view_list():
	global CURR_MSG
	list_id = int(request.args.get('id'))
	for shopping_list in shopping_lists:
		if shopping_list.id == list_id:
			msg = CURR_MSG
			CURR_MSG = ""
			return render_template(
				'shopping_list.html', shopping_list=shopping_list,
				items=shopping_list.items, has_items=len(shopping_list.items) > 0,
				has_massage=len(msg) > 0, msg=msg
			)
	CURR_MSG = "For some reason, we could not find the shopping list you specified!"
	return redirect('/')

@app.route("/remove_item")
def remove_item():
	global CURR_MSG
	connection, cursor = get_cursor()
	list_id = int(request.args.get('list_id'))
	item_id = int(request.args.get('item_id'))
	for shopping_list in shopping_lists:
		if shopping_list.id == list_id:
			for item in shopping_list.items:
				if item.id == item_id:
					shopping_list: PurchasePlan
					code = shopping_list.remove_item(cursor, connection, item.id, user)
					if code != 1:
						CURR_MSG = f"We could not remove item from shopping list: {MSG_REMOVE_ITEM[code]}"
					return redirect(f'/view_list?id={shopping_list.id}')
			CURR_MSG = "For some reason, we could not find the item you specified!"
			redirect(f'/view_list?id={shopping_list.id}')
	CURR_MSG = "For some reason, we could not find the shopping list you specified!"
	return redirect('/')

@app.route("/remove_list")
def remove_list():
	global CURR_MSG
	list_id = int(request.args.get('id'))
	connection, cursor = get_cursor()
	if PurchasePlan.check_user_plan(cursor, user.id, list_id):
		PurchasePlan.delete_purchase_plan(cursor, connection, list_id)
	else:
		CURR_MSG = "You cannot delete the specified list!"
	return redirect('/')


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5004)