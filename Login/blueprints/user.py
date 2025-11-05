from flask import Blueprint, redirect, url_for, session, request, render_template, flash
from DataBase.models import app, Users, db

bp = Blueprint("user", __name__)


@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            session["password"] = password
            session["email"] = email

            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            found_user.password = password

            db.session.commit()

            flash("Data saved!", "info")
            return render_template("user.html", user=user, email=email, password=password)
        else:
            found_user = Users.query.filter_by(name=user).first()
            password = found_user.password
            email = found_user.email

            return render_template("user.html", user=user, email=email, password=password)
    else:
        return redirect(url_for("login"))