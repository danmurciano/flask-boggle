from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.config["SECRET_KEY"] = "w57h63ff"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.debug = True
debug = DebugToolbarExtension(app)

game = Boggle()


@app.route("/")
def home_page():
    board = game.make_board()
    session["board"] = board
    high_score = session.get("high_score", 0)
    plays = session.get("plays", 0)
    return render_template("home.html", board=board, high_score=high_score, plays=plays)


@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    result = game.check_valid_word(board, word)
    return jsonify({"result": result})


@app.route("/update-score", methods=["POST"])
def update_score():
    score = request.json["score"]
    high_score = session.get("high_score", 0)
    plays = session.get("plays", 0)

    session["plays"] = plays + 1
    session["high_score"] = max(score, high_score)

    return jsonify(brokeRecord = score > high_score)
