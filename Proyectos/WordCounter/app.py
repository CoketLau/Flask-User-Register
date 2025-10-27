from flask import render_template, Flask, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        text = request.form["txt"]

        return redirect(url_for("home", chars=text))
    
    else:
        chars = request.args.get("chars")

        if chars:
            return render_template("home.html", chars=len(chars))
        else:
            return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")