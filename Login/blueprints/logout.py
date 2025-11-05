from flask import Blueprint, redirect, url_for, session, render_template, flash
from DataBase.models import app


bp = Blueprint("logout", __name__)


@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)
        session.pop("password", None)
        session.pop("email", None)

        return redirect(url_for("home"))
    else:
        flash("Login first!", "info")
        return render_template("login.html")