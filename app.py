from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_session import Session
from tempfile import mkdtemp
from main import * 
from AI import *
from evaluating import *
from gameclass import game

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/", methods=["GET", "POST"])
def index():

    if "new_game_options" in session:
        new_game()
        
    if "game" not in session:
        no_game = game()
        session["game"] = no_game
        return render_template("board.html", game = session["game"])

    if request.method == "POST":

        if request.form.get("NEW GAME") == "NEW GAME":
            session["game"].new = True
            return render_template("board.html", game=session["game"])


    session["game"].new = False

    first_move()

    if session["game"].made_move: #There are minor bugs (i.e no sound on safari) with sound that will be looked into later
        move_sound = True
    else: 
        move_sound = False 


    computer_move(move_sound) 

    session["game"].board_score = update_score(session["game"].board, session["game"].players)

    if check_end(session["game"].board_score, session["game"].board):
        return render_template("board.html", game=session["game"])

    session["made_move"] = False 

    return render_template("board.html", game=session["game"], sound = move_sound)



@app.route("/processing", methods=["GET", "POST"])
def process_newgame():
    data = request.get_json()
    session["new_game_options"] = data["data"]
    new_game()

    return "success", 200
    
@app.route("/newround", methods=["GET", "POST"])
def new_round():
    session["game"].board = generate_board()
    session["game"].moves = 0
    session["game"].made_move = False
    session["game"].board_score = 0
    session["game"].end = False
    session["game"].round += 1
    return redirect(url_for("index"))

@app.route("/play/<int:col>/", methods=["GET", "POST"])
def playing(col):
    make_move(col, session["game"].board , session["game"].players, session["game"].p1_move)
    session["game"].made_move = True
    session["game"].p1_move = not session["game"].p1_move 
    session["game"].moves += 1
    return redirect(url_for("index"))


"""Helper functions"""
def comp_play():
    col = computer_play(session["game"].board, session["game"].players, session["game"].moves)
    playing(col)
        

def new_game():

    start_game = game()
    session["game"] = start_game
    session["game"].legal_move = True

    if session["new_game_options"][0][0] == 1:
        session["game"].computer = True

    elif session["new_game_options"][0][1] == 1:
        session["game"].computer  = False
    
    if session["new_game_options"][1][0] == 0:
        session["game"].players = [player(1, "X"), player(2, "O")]
    elif session["new_game_options"][1][0] == 1:
         session["game"].players = [player(1, "O"), player(2, "X")]
        
    session.pop("new_game_options")
    return True

"""A score has a max of 17 (the minimum number of counters required to win)"""
def check_end(score, board_matrix):
    if score >= HAS_WON:
        flash("Player 1 wins!")
        session["game"].player_scores[0] += int((HEIGHT*WIDTH - session["game"].moves)/2)

        return True  
    
    elif score <= -HAS_WON:
        if session["game"].computer:
            flash("Computer wins!")
        else:
            flash("Player 2 wins!")
        session["game"].player_scores[1] += int((HEIGHT*WIDTH - session["game"].moves)/2)

        return True
        

    elif draw(board_matrix):
        flash("Draw!")
    
    else:
        return False

    session["game"].legal_move = False
    session["game"].end = True
    return True

"""This function decides which player moves first"""
def first_move():
    if session["game"].moves == 0 and session["game"].round != 1:
        if session["game"].first_move == 1:
            session["game"].p1_move = False 
        else:
            session["game"].p1_move = True

        session["game"].fist_move = session["game"].first_move % 2 + 1
    return 

def computer_move(move_sound):
    if session["game"].computer:

        if session["game"].made_move:
            session["game"].made_move = False
            session["game"].legal_move = False 
            return render_template("board.html", game=session["game"], sound = move_sound)

        if not session["game"].p1_move:
            comp_play()
            session["game"].legal_move = True
    return 
