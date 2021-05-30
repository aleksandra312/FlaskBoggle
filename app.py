from boggle import Boggle
from flask import Flask, request, render_template, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()
BOARD = "board"

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """Display the boggle game board."""
    board = boggle_game.make_board()
    session[BOARD] = board
    flash("Lets play a Boggle game!", "success")
    return render_template("home.html", board=board)


@app.route("/check-word")
def check_word():
    """Validate input word."""
    word = request.args["word"]
    board = session[BOARD]
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})
