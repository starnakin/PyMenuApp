from kivy.uix.label import Label
import mysql.connector
import json

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp

db_config = json.load(open("./db.json"))

user = db_config["user"]
password = db_config["password"]
ip = db_config["ip"]
port = db_config["port"]
db_name = db_config["db_name"]

mydb = mysql.connector.connect(
  host=ip,
  user=user,
  password=password,
  database=db_name
)

mycursor = mydb.cursor()

class WindowManager(ScreenManager):
    pass

class MainWindow(Screen):
    def already_connected(self):
        file = json.load(open("./connection.json"))
        if file["username"] != "" and file["family"] != "":
            self.parent.current="connected"
        else:
            self.parent.current="connection"

class AddMemberWindow(Screen):
    def add_member(self, username):
        mycursor.execute("INSERT INTO familys (family, username, password) VALUES (%s, %s, %s)", (json.load(open("./connection.json"))["family"], username.text, ""))
        mydb.commit()
        self.parent.current="connected"

class ConnectionWindow(Screen):
    def connection(self, family, username, password):
        mycursor.execute("SELECT password FROM familys WHERE (family = %s AND username = %s)", (family.text, username.text))
        result = mycursor.fetchall()
        if len(result) > 0:
            if(result[0][0] == password.text and result[0][0] != ""):
                pass
            else:
                mycursor.execute("INSERT INTO familys (family, username, password) VALUES (%s, %s, %s)", (family.text, username.text, password.text))
                mydb.commit()
        else:
            mycursor.execute("INSERT INTO familys (family, username, password) VALUES (%s, %s, %s)", (family.text, username.text, password.text))
            mydb.commit()
        self.parent.current="connected"

class AddWindow(Screen):
    def add_to_list(self, element, quantity):
        family=json.load(open("./connection.json"))["family"]
        if element.text == "":
            return
        if quantity.text == "":
            quantity=1
        else:
            quantity=int(quantity.text)
        mycursor.execute("INSERT INTO objects (family, objects, quantity) VALUES (%s, %s, %s)", (family, element.text, quantity))
        mydb.commit()
        self.manager.get_screen('connected').update()
        self.parent.current="connected"

class CreateFamilyWindow(Screen):
    def create_family(self, family, username):
        mycursor.execute("INSERT INTO familys (family, username, password) VALUES (%s, %s, %s)", (family.text, username.text, ""))
        mydb.commit()
        #json.dump({"family": family.text, "username":username.text}, json.load(open("./connection.json", "w")))
        self.parent.current="connected"

class ListeLayout(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            mycursor.execute("SELECT * FROM objects WHERE family = '{}'".format(json.load(open("./connection.json"))["family"]))
            result = mycursor.fetchall()
        except:
            result=[]
        for i in result:
            layout=BoxLayout(height=dp(20), padding=(dp(20), dp(20), dp(20), dp(20)), spacing=dp(10))
            layout.add_widget(Button(text="-"))
            label = Label(text=str(i[1]))
            layout.add_widget(label)
            layout.add_widget(Button(text="+"))
            self.add_widget(layout)

    def get_quantity(self):
        print("self.ids.name_label.text")
    
    def add_element(self, ):
        pass

class ConnectedWindow(Screen):
    pass


class PyMenuApp(App):
    def build(self):
        return Builder.load_file("window.kv")

PyMenuApp().run()