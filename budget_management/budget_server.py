from flask import Flask, request, render_template, url_for, redirect
from flask_mysqldb import MySQL
from config import Config
from models.budget import Budget
from models.category import Category
from models.expense import Expense
from models.group import Group


app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)


def get_cursor():
    return mysql.connection.cursor()


@app.route("/budget_test")
def hello_world():
	return "<p>There will be a budget management service!</p>"


@app.route('/')
def redirect_to_budgets():
    return redirect(url_for('all_budgets'))


@app.route('/all_budgets')
def all_budgets():
    cursor = get_cursor()
    group_id = 1
    budgets = Budget.get_all_budgets_by_group(cursor, group_id)
    group_name = Group.get_group_name_by_id(cursor, group_id)
    return render_template('budgets.html', budgets=budgets, group_id=group_id, group_name=group_name)


@app.route('/add_budget', methods=['POST'])
def add_budget():
    if request.method == 'POST':
        group_id = request.form['group_id']
        budget_name = request.form['budget_name']
        total_budget = request.form['total_budget']
        cursor = get_cursor()

        Budget.add_budget(cursor, group_id, budget_name, total_budget)
        mysql.connection.commit()

        return redirect(url_for('all_budgets'))


@app.route('/update_budget/<int:budget_id>', methods=['GET', 'POST'])
def update_budget(budget_id):
    if request.method == 'POST':
        budget_name = request.form['budget_name']
        total_budget = request.form['total_budget']
        cursor = get_cursor()

        Budget.update_budget(cursor, budget_id, budget_name, total_budget)
        mysql.connection.commit()
        return redirect(url_for('all_budgets'))

    cursor = get_cursor()
    budget = Budget.get_budget_by_id(cursor, budget_id)
    return render_template('update_budget.html', budget=budget)


@app.route('/delete_budget/<int:budget_id>', methods=['GET'])
def delete_budget(budget_id):
    cursor = get_cursor()
    Budget.delete_budget(cursor, budget_id)
    mysql.connection.commit()
    return redirect(url_for('all_budgets'))


@app.route('/expenses/<int:budget_id>')
def view_expenses(budget_id):
    cursor = get_cursor()
    budget = Budget.get_budget_by_id(cursor, budget_id)
    expenses = Expense.get_all_expenses_by_budget(cursor, budget_id)
    spent_this_month = Expense.sum_current_expenses_this_month(cursor, budget_id)
    categories = Category.get_all_categories(cursor)
    return render_template('expenses.html', expenses=expenses, categories=categories, budget=budget, spent_this_month=spent_this_month)


@app.route('/add_expense/<int:budget_id>', methods=['POST'])
def add_expense(budget_id):
    if request.method == 'POST':
        description = request.form['description']
        price = request.form['price']
        amount = request.form['amount']
        expense_type = request.form['expense_type']
        category_id = request.form['category_id']
        user_id = 1
        cursor = get_cursor()

        Expense.add_expense(cursor, budget_id, description, price, amount, expense_type, category_id, user_id)
        mysql.connection.commit()
        return redirect(url_for('view_expenses', budget_id=budget_id))


@app.route('/update_expense/<int:expense_id>', methods=['GET', 'POST'])
def update_expense(expense_id):
    if request.method == 'POST':
        description = request.form['description']
        price = request.form['price']
        amount = request.form['amount']
        expense_type = request.form['expense_type']
        category_id = request.form['category_id']
        budget_id=request.form['budget_id']
        cursor = get_cursor()

        Expense.update_expense(cursor, expense_id, description, price, amount, expense_type, category_id)
        mysql.connection.commit()
        return redirect(url_for('view_expenses', budget_id=budget_id))

    cursor = get_cursor()
    expense = Expense.get_expense_by_id(cursor, expense_id)
    categories = Category.get_all_categories(cursor)
    return render_template('update_expense.html', expense=expense, categories=categories)


@app.route('/delete_expense/<int:expense_id>/<int:budget_id>', methods=['GET'])
def delete_expense(expense_id, budget_id):
    cursor = get_cursor()
    Expense.delete_expense(cursor, expense_id)
    mysql.connection.commit()
    return redirect(url_for('view_expenses', budget_id=budget_id))


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5001, debug=True)
     