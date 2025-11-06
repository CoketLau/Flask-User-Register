from flask import Blueprint, redirect, url_for, session, request, render_template, flash
from DataBase.models import app, Users


bp = Blueprint("login", __name__, template_folder="../Templates")


@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" in session:
        return redirect(url_for("user"))
    else:
        if request.method == "POST":
            password = request.form["password"]
            user = request.form["user"]
            found_user = Users.query.filter_by(name=user).first()

            if found_user:
                if found_user.password == password:
                    session.permanent = True
                    session["user"] = user
                    session["password"] = password
                    session["email"] = found_user.email

                    email = found_user.email
                    
                    return render_template("user.html", user=user, email=email, password=password)
                else:
                    flash("Incorrect info", "info")
                    return render_template("login.html")

            else:
                flash("Incorrect info", "info")
                return render_template("login.html")
            
        else:
            return render_template("login.html")
