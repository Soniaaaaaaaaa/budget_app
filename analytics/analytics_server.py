from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import os


app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)


@app.route("/analytics_text")
def hello_world():
	return "<p>There will be an analytics service!</p>"


# @app.route('/report', methods=['GET'])
# def generate_report():
# 	report = Report.generate_report()
# 	return jsonify(report)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
