from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "key" #Dar una key pq ns
app.permanent_session_lifetime = timedelta(minutes=5)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Data_Base = SQLAlchemy(app)


class Users(Data_Base.Model): #clase usada para cada vez que registremos un usuario
    id = Data_Base.Column(Data_Base.Integer, primary_key=True)
    name = Data_Base.Column(Data_Base.String(100)) #String(100) = name no puede ser mayor a 100 caracteres
    email = Data_Base.Column(Data_Base.String(100)) #String(100) = email no puede ser mayor a 100 caracteres

    def __init__(self, name, email=""): #Crear un usuario
        self.name = name
        self.email = email



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user

        found_user = Users.query.filter_by(name=user).first() #Busca un usuario en la base de datos
        if found_user: #Si está hace esto:
            session["email"] = found_user.email
        else: #Si no está crea uno
            usr = Users(user, "")
            Data_Base.session.add(usr)
            Data_Base.session.commit()

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
        session.pop("email", None)
        flash("You have logged out!", "info")
    return redirect(url_for("login"))



@app.route("/del", methods=["POST", "GET"])
def delete():
    if "user" in session:
        user = session["user"]

        if user == "Admin":
            if request.method == "POST":
                deletion = request.form["deletion"]
                found_user = Users.query.filter_by(name=deletion).first()
                
                if found_user:
                    if found_user.name == "Admin":
                        flash("You can't delete Admin!")
                        return render_template("delete.html")
                    else:
                        Data_Base.session.delete(found_user)
                        Data_Base.session.commit()

                        flash("User deleted succesfully!", "info")
                        return redirect(url_for("view"))
                else:
                    flash("User not found", "info")
                    return redirect(url_for("view"))
            else:
                return render_template("delete.html")
        
        else:
            flash("You are not an admin")
            return redirect(url_for("user"))
    
    else:
        flash("Please log in")
        return redirect(url_for("login"))



@app.route("/user", methods=["POST", "GET"])
def user():
    email = None #Hay que declarar la variable email
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email

            Data_Base.session.commit()

            session["email"] = email
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]


        return render_template("usuario.html", contenido=user, email=email)
    else:
        return redirect(url_for("login"))



@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())


if __name__ == "__main__":
    with app.app_context():
        Data_Base.create_all()
    app.run(debug=True, host="0.0.0.0")