from flask import Blueprint, redirect, url_for, session, render_template, flash
from DataBase.models import app, Users


bp = Blueprint("view", __name__, template_folder="../Templates")


@app.route("/view")
def view():
    if session["user"] == "Admin":
        return render_template("view.html", values=Users.query.all())
    else:
        flash("You are not an Admin!", "info")
        return redirect(url_for("user"))
