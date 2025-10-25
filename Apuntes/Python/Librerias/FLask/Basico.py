from flask import render_template, Flask, redirect, url_for

app = Flask(__name__) #Ahora mismo name es "Básico.py, pero si importamos este archivo __name__ es solo "Básico"



#Lo de abajo crea una ruta
@app.route("/") #Sin poner nada te mandará a la casa, pero si pones por ejemplo (/Home) solo te mandará a Home si lo pones manual
def home(): #Definimos la funcion que devuelve el archivo HTML
    HTML_FILE = "index.html"
    return render_template(HTML_FILE) #Renderizamos lo de dentro del archivo y hace el return, devolviendo la página

@app.route("/<name>")#Lo que ponga despues de la barrita se pasa a user como parámetro
def user(name):
    if name == "Admin!":
        return "<hi>You are the admin :)<h1>"
    else:
        return f"¡Hola {name}!"


@app.route("/Admin")
def admin():
    return redirect(url_for("user", name="Admin!")) #Así hacemos que cuendo lo redireccionemos a user tenga un parámetro


if __name__ == "__main__": #Hace que SOLO SE PUEDA EJECUTAR EL SERVIDOR DIRECTAMENTE, SOLO DESDE ESTE ARCHIVO

    app.run(host="0.0.0.0", port=5000, debug=True) #El 0.0.0.0 hace que todos los del wifi se conecten, entonces ya no es solo de un equipo (Local host)
            #Host dice a qué ip escuchar, con 0.0.0.0 escuchará todas las ips dentro de la misma red