from flask import Flask, render_template, request
import Encripter

app = Flask(__name__)
Chars = Encripter.characters()
Key = Encripter.Key(Chars)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/encript", methods=["POST", "GET"])
def encript():
    if request.method == "GET":
        return render_template("encript.html")
    elif request.method == "POST":
        MSG = request.form["text"]
        MSG_En = Encripter.Encript(MSG, Key, Chars)

        return render_template("encript.html", output=MSG_En)


@app.route("/decript", methods=["POST", "GET"])
def decript():
    if request.method == "GET":
        return render_template("decript.html")
    elif request.method == "POST":

        MSG = request.form["text"]
        MSG_Dec = Encripter.Decript(MSG, Key, Chars)

        return render_template("decript.html", output=MSG_Dec)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)