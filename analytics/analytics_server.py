from flask import Flask, request
from flask_mysqldb import MySQL
from config import Config
from models.report import Report
from models.expense import Expense


app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)
 

def get_cursor():
    return mysql.connection.cursor()


@app.route('/expenses_by_group', methods=['GET'])
def get_expenses_by_group():
    data = request.json
    cursor = get_cursor()
    expenses = Expense.get_expenses_by_group(cursor, group_id=data['group_id'])

    return expenses
     

@app.route('/reports_by_group', methods=['GET'])
def get_reports_by_group():
    data = request.json
    cursor = get_cursor()
    reports = Report.get_reports_by_group(cursor, group_id=data['group_id'])

    return reports


@app.route('/report_by_id', methods=['GET'])
def get_report_by_id():
    data = request.json
    cursor = get_cursor()
    report = Report.get_report_by_id(cursor, report_id=data['report_id'])

    return report


@app.route('/create_report', methods=['POST'])
def create_report():
    data = request.json
    cursor = get_cursor()

    Report.create_report(cursor, group_id=data['group_id'], report_data=data['report_data'])
    mysql.connection.commit()

    return {'status': 'success'}


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5002)