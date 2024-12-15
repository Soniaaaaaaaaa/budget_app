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

@server.route("/login", methods=["GET"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
        
    cur = mysql.connection.cursor()
    user_data = User.get_user_by_email(cur, email)
        
    if user_data[1] == email and user_data[2] == password:
        token = create_jwt(email, os.environ.get("JWT_SECRET"))
        return {
            "id": user_data[0],
            "status":"success",
            "token": token
            }
    else:
        return {"status": "Invalid credentials"} #401

@server.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data["email"]
    password = data["password"]
    cur = mysql.connection.cursor()
    user_data = User.get_user_by_email(cur, email)
        
    if user_data:
        return  {"status":"email already exists"}
        
    User.create_user(cur, email, password)
    mysql.connection.commit()
    cur.close()
    return {"status": "success"}

@server.route("/profile", methods=["GET", "POST"])
def profile():
    data = request.json
    user_id = data["id"]
    cur = mysql.connection.cursor()
    user_data = User.get_user_by_id(cur, user_id)
    if request.method == "POST":
        current_password = data["current_password"]
        new_password = data["new_password"]
        username = data["username"]
        if current_password is not None and new_password is not None and user_data[2] == current_password:
                User.update_passwd(cur, user_data[1], new_password)
                mysql.connection.commit()
                return {"status": "success"}
        elif username is not None:
            User.update_username(cur, user_id, username)
            mysql.connection.commit()
            return {"status": "success"}
        else:
            return {"status": "Invalid current password"}
        
    else:
        return {
            "email": user_data[1],
            "username": user_data[3],
            "group_id":user_data[4]
        }

@server.route("/group", methods=["GET", "POST"]) # list groups ad user status and username
def group():
    data = request.json
    user_id = data["id"]
    cur = mysql.connection.cursor()
    info  = User.groups_info(cur, user_id) 
    if request.method == "POST":
        group_name = data["group_name"]
        if info is not None:
            User.groups_updata(cur, info[2], group_name)
            mysql.connection.commit()
            return {"status": "success"}
    else:
        mysql.connection.commit()     
        return {"group_name": info[0], 
                "group_status": info[1]
                }

@server.route("/create_group", methods=["POST"])
def create_group():
    data = request.json
    user_id = data["id"]
    name = data["group_name"]
    cur = mysql.connection.cursor()
    group_id = User.create_group(cur, user_id, name)
    mysql.connection.commit()  
    return {"group_id":group_id}
   

@server.route("/add_member", methods=["POST"])
def add_member():
    data = request.json
    user_id = data["id"]
    member_email = data["email"]
    cur = mysql.connection.cursor()
    User.add_member(cur, user_id, member_email)
    mysql.connection.commit()  
    return {"status": "success"} 

@server.route("/delete_member", methods=["POST"])
def delete_member():
    data = request.json
    member_email = data["email"]
    cur = mysql.connection.cursor()
    User.delete_member(cur, member_email)
    mysql.connection.commit()  
    return {"status": "success"} 
    
@server.route("/list_members", methods=["GET"])
def list_member():
    data = request.json
    group_id = data["group_id"]
    cur = mysql.connection.cursor()
    group_list = User.get_group_members(cur, group_id )
    mysql.connection.commit()  
    return jsonify(group_list)

@server.route("/validate", methods=["POST"])
def validate(): 
    data = request.json
    token = data["token"]
    decoded_jwt = decode_jwt(token, os.environ.get("JWT_SECRET"))
    if decoded_jwt:
         return {"status": "success"}
    else: return {"status": "Unauthorized"}


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)



  #MySQLdb.OperationalError: (1046, 'No database selected') FIX: export MYSQL_DB="budget_app"
     # File "/home/sofayankovich0106/.local/lib/python3.12/site-packages/jwt/utils.py", line 22, in force_bytes
    # raise TypeError("Expected a string value") FIX: export JWT_SECRET="561ee36ac433f36ae868a5a88278dc9f09cfa3c5c0d976cfe9611db152195fdf"