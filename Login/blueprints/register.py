from flask import Blueprint, redirect, url_for, session, request, render_template, flash
from DataBase.models import app, Users, db

bp = Blueprint("register", __name__)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]
        found_User = Users.query.filter_by(name=user).first()

        if found_User:
            flash("Username in use", "info")
            return render_template("register.html")
        else:
            session["user"] = user
            session["password"] = password
            
            New_User = Users(user, password, email="")

            db.session.add(New_User)
            db.session.commit()

            return redirect(url_for("user"))
    else:
        return render_template("register.html")