from DataBase.models import app, db
from blueprints import home, user, login, register, delete, view, logout


app.root_path = "Login"
blueprints = [home, user, login, register, delete, view, logout]


for bp in blueprints:
    app.register_blueprint(bp.bp)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")