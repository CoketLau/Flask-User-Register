from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "key" #Dar una key pq ns
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user

        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        else:
            return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("You have logged out!", "info")
    return redirect(url_for("login"))

@app.route("/User")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("usuario.html", contenido=user)
    else:
        return redirect(url_for("login"))

    


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")