from flask import Blueprint, redirect, url_for, session
from DataBase.models import app

bp = Blueprint("home", __name__)

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("user"))
    else:
        return redirect(url_for("login"))