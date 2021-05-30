from boggle import Boggle
from flask import Flask, request, render_template, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()
BOARD = "board"
NUM_PLAYS = "nplays"
HIGH_SCORE = "highscore"

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """Display the boggle game board."""
    board = boggle_game.make_board()
    session[BOARD] = board
    highscore = session.get(HIGH_SCORE, 0)
    nplays = session.get(NUM_PLAYS, 0)
    flash("Lets play a Boggle game!", "success")
    return render_template("home.html", board=board, highscore=highscore, nplays=nplays)


@app.route("/check-word")
def check_word():
    """Validate input word."""
    word = request.args["word"]
    board = session[BOARD]
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Post the highest score and number of times the user played the game."""
    score = request.json["score"]
    
    highscore = session.get(HIGH_SCORE, 0)
    nplays = session.get(NUM_PLAYS, 0)
    
    session[NUM_PLAYS] = nplays + 1
    session[HIGH_SCORE] = max(score, highscore)
    return jsonify(newHighScore = score > highscore)
