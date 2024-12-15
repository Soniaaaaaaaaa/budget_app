import os


class Config:
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER= os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = "budget_app"
    MYSQL_PORT = os.environ.get("MYSQL_PORT")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'budget.app1234@gmail.com'
    MAIL_PASSWORD = 'iwqb crbb nday cict'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False