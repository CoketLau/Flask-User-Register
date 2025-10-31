from flask import render_template, redirect, url_for, session, flash, Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = "key"
app.permanent_session_lifetime = timedelta(minutes=10)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.root_path}/DataBase/Database.sqlite3"    
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



@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("user"))
    else:
        return redirect(url_for("login"))



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
                    flash("Incorrect password", "info")
                    return render_template("login.html", msg="Incorrect password")

            else:
                session["user"] = user
                session["password"] = password

                db.session.add(Users(user, password, ""))
                db.session.commit()
                return redirect(url_for("user"))
            
        else:
            return render_template("login.html")



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



@app.route("/view")
def view():
    if session["user"] == "Admin":
        return render_template("view.html", values=Users.query.all())
    else:
        flash("You are not an Admin!", "info")
        return redirect(url_for("user"))



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



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")