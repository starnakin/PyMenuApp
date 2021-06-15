import mysql.connector
import json

db_config = json.load(open("./db.json"))

user = db_config["user"]
password = db_config["password"]
ip = db_config["ip"]
port = db_config["port"]
db_name = db_config["db_name"]

mydb = mysql.connector.connect(
  host=ip,
  user=user,
  password=password
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE "+ db_name)

mydb = mysql.connector.connect(
  host=ip,
  user=user,
  password=password,
  database=db_name
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE familys (family TEXT(255), username TEXT(255), password TEXT(255))")
mycursor.execute("CREATE TABLE objects (family TEXT(255), objects TEXT(255), quantity INT(255))")