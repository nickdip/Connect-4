from board import *
from main import player

"""This creates a new game when playing on the web"""
class game():
    def __init__(self, 
                 p1_move = True, 
                 board = generate_board(), 
                 new = False, 
                 legal_move = False, 
                 computer = None, 
                 player_scores = [0,0], 
                 players = [player(1, "X"), player(2, "O")],
                 made_move = False,
                 moves = 0, 
                 end = False,
                 round = 1,
                 first_move = 1,
                 end_sound = False,
                 move_sound = False):
        self.board = board
        self.p1_move = p1_move
        self.new = new
        self.legal_move = legal_move
        self.computer = computer
        self.player_scores = player_scores 
        self.players = players
        self.made_move = made_move
        self.moves = moves
        self.end = end
        self.first_move = first_move
        self.round = round
        self.end_sound = end_sound
        self.move_sound = move_sound


