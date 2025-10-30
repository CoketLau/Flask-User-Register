from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "key" #Dar una key pq ns
app.permanent_session_lifetime = timedelta(days=5) #Ponemos cuanto tiempo se guarda el data permanente

#La session normal dura solamente el tiempo que tengamos abierto el browser

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user #Guarda user en session

        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        else:
            return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/User")
def user():
    if "user" in session: #miramos si existe user
        user = session["user"]
        return render_template("usuario.html", contenido=user)
    else:
        return redirect(url_for("login"))

    


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")