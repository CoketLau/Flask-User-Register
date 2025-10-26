from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def message():
    if request.method == "GET":
        return render_template("Input.html")
    
    elif request.method == "POST":
        message = request.form["msg"] #Nombre del input del html

        return render_template("Input.html", output=f"Hi {message}")

if __name__ == "__main__":
    app.run(debug=True)