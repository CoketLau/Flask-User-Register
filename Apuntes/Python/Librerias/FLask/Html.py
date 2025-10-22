from flask import render_template, Flask

app = Flask(__name__)



@app.route("/")
def home():
    HTML_FILE = "index.html"
    return render_template(HTML_FILE)


@app.route("/<user>")
def usuario(user):
    HTML_FILE = "usuario.html"
    return render_template(HTML_FILE, contenido=user) #El contenido=user hace que dentro del html el {{contenido}} se cambie por el user, es un parámetro

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)