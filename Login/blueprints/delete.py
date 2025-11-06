from flask import Blueprint, redirect, url_for, session, request, render_template, flash
from DataBase.models import app, Users, db


bp = Blueprint("delete", __name__, template_folder="../Templates")


@app.route("/delete", methods=["POST", "GET"])
def delete():
    if "user" in session:
        user = session["user"]

        if user == "Admin":
            if request.method == "POST":
                deletion = request.form["user"]
                found_user = Users.query.filter_by(name=deletion).first()

                if found_user:
                    if found_user.name == "Admin":
                        flash("You can't delete Admin!")
                        return render_template("delete.html")
                    else:
                        db.session.delete(found_user)
                        db.session.commit()

                        flash("User deleted succesfully!", "info")
                        return redirect(url_for("view"))
                else:
                    flash("User not found", "info")
                    return redirect(url_for("view"))
            else:
                return render_template("delete.html")
        else:
            flash("You are not an Admin!")
            return redirect(url_for("user"))
    else:
        flash("Login first!", "info")
        return redirect(url_for("login"))
