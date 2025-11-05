from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>Hola {usr}!</h1>"


if __name__ == "__main__":
    app.run()