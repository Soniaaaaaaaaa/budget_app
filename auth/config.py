import os
class Config:
    #MYSQL_HOST = 'host.docker.internal'
    #MYSQL_USER= 'sofayankovich0106'
    #MYSQL_PASSWORD = ''
    #MYSQL_DB = 'budget_app'
    #MYSQL_PORT =  3306
    #JWT_SECRET='561ee36ac433f36ae868a5a88278dc9f09cfa3c5c0d976cfe9611db152195fdf'

    # for test 
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER= os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = "budget_app"
    MYSQL_PORT = os.environ.get("MYSQL_PORT")
    