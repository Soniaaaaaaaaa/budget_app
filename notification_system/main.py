from flask import Flask, request, render_template, redirect
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from config import Config
from time import sleep

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)
mail = Mail(app)

def get_cursor():
	connection = mysql.connection
	cursor = connection.cursor()
	return connection, cursor

def get_unsent_messages(cursor):
    query = "SELECT notification_id, username, email, message, recieved_date FROM notification JOIN user ON user.user_id = notification.user_id WHERE NOT is_sent"
    cursor.execute(query)
    return cursor.fetchall()

def mark_as_sent(connection, cursor, notificaion_id: int):
    try:
        query = "UPDATE notification SET is_sent = True WHERE notification_id = %s"
        cursor.execute(query, (notificaion_id,))
        connection.commit()
    except:
        pass

def main():
    cols = ["notification_id", "username", "email", "message", "recieved_date"]
    while True:
        connection, cursor = get_cursor()
        notifications = get_unsent_messages(cursor)
        for row in notifications:
            row = {col: val for col, val in zip(cols, row)}
            msg_id = row["notification_id"]
            username = row["username"]
            email = row["email"]
            text = row["message"]
            date = row["recieved_date"]
            msg = Message(
                subject='Notififcation from budget app!', 
                sender=Config.MAIL_USERNAME,
                recipients=[email]
                )
            msg.body = f"Hi, {username}! Budget app sent you a notification at {date}\n\n{text}"
            mail.send(msg)
            mark_as_sent(connection, cursor, msg_id)
        sleep(60)


if __name__ == '__main__':
    with app.app_context():
        main()