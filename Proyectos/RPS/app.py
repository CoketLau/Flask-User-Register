from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def home():
    Home_Html = render_template("home.html")

    return Home_Html

@app.route("/Play/<choise>")
def Play(choise):
    PosiblePlays = ["Rock", "Paper", "Scissors"]
    Ran_Choise = random.randint(0, 2)
    Outcome = "Tie! :/"


    if choise == "Paper":
        if PosiblePlays[Ran_Choise] == "Rock":
            Outcome = "win! :D"
        elif PosiblePlays[Ran_Choise] == "Scissors":
            Outcome = "loose! :("
    

    elif choise == "Rock":
        if PosiblePlays[Ran_Choise] == "Scissors":
            Outcome = "win :D"
        elif PosiblePlays[Ran_Choise] == "Paper":
            Outcome = "loose :("
    

    elif choise == "Scissors":
        if PosiblePlays[Ran_Choise] == "Paper":
            Outcome = "win :D"
        elif PosiblePlays[Ran_Choise] == "Rock":
            Outcome == "loose :("



    return render_template("Play.html", som=choise, attack=PosiblePlays[Ran_Choise], state=Outcome)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    #USA NGROK HTTP 5000 PARA HACER EL DOMINIO PÚBLICO
