from flask import Flask, jsonify, make_response, redirect,  request, render_template, url_for
from flask_mysqldb import MySQL
from models.user import User
from utils.jwt import create_jwt, decode_jwt
from config import Config
import os
import requests

server = Flask(__name__)
server.config.from_object(Config)

mysql = MySQL(server)

@server.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        cur = mysql.connection.cursor()
        user_data = User.get_user_by_email(cur, email)
        
        if user_data[1] == email and user_data[2] == password:
            token = create_jwt(email, os.environ.get("JWT_SECRET"), True)
            response = make_response(redirect(url_for("profile", email=email)))
            response.set_cookie("user_id", str(user_data[0]))
            response.set_cookie("user_token", token)
            return response
        else:
            return "Invalid credentials", 401
    return render_template("login.html")

@server.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        user_data = User.get_user_by_email(cur, email)
        
        if user_data:
            return "Email already exists", 409
        
        User.create_user(cur, email, password)
        mysql.connection.commit()
        cur.close()
        return render_template("login.html"), 200
    
    return render_template("register.html")

@server.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = request.cookies.get("user_id") 
    if not user_id: 
        return "id not provided", 400 
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        cur = mysql.connection.cursor()
        user_data = User.get_user_by_id(cur, user_id)
        if user_data[2] == current_password:
            try:
                User.update_passwd(cur, user_data[1], new_password)
                mysql.connection.commit()
                message = "Password successfully changed"
                success = True
            except Exception as e:
                message = f"Error updating password: {str(e)}"
                success = False
        else:
            message = "Invalid current password"
            success = False
        return render_template(
            "profile.html", message=message, success=success,
        )
    return render_template("profile.html")

@server.route("/profile", methods=["GET", "POST"])
    
@server.route("/validate", methods=["POST"])
def validate():
    token = request.headers.get("Authorization", "").split(" ")[1]
    decoded_jwt = decode_jwt(token, os.environ.get("JWT_SECRET"))
    if decoded_jwt:
        return decoded_jwt, 200
    return "Unauthorized", 403

@server.route("/menu")
def menu():
    service = request.args.get("service")
    user_token = request.cookies.get("user_token")
    user_id = request.cookies.get("user_id")

    if not user_token or not user_id:
        return "Unauthorized", 401

    if service == "budget":
        data = call_budget_service(user_token, user_id)
    elif service == "profile":
        return redirect(f"/profile?user_id={user_id}")
    else:
        return "Service not found", 404

    return jsonify(data)

def call_budget_service(user_token, user_id):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(f"http://localhost:5001/all_budgets?user_id={user_id}", headers=headers)
    return response.json()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5007)



  #MySQLdb.OperationalError: (1046, 'No database selected') FIX: export MYSQL_DB="budget_app"
     # File "/home/sofayankovich0106/.local/lib/python3.12/site-packages/jwt/utils.py", line 22, in force_bytes
    # raise TypeError("Expected a string value") FIX: export JWT_SECRET="561ee36ac433f36ae868a5a88278dc9f09cfa3c5c0d976cfe9611db152195fdf"