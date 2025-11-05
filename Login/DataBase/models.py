from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "key"
app.permanent_session_lifetime = timedelta(minutes=10)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.root_path}/Database.sqlite3"    
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False





db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, password, email=""):
        self.name = name
        self.password = password
        self.email = email