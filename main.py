from helpers import *
from AI import *
from connect import *
from copy import deepcopy
from evaluating import *
from board import *
import random



"""Notes; efficiency in generate function with step (repeats check)

Remove some values from connections_list in evaluation to narrow the search

Delete draw from connect.py"""

class player():
    def __init__(self, id, symbol, score = 0.0, computer = False):
        if isinstance(id, int):
            self.id = id
        else:
            raise ValueError("Person ID must be an integer")
        if isinstance(symbol, str):
            if symbol in SYMBOLS:
                self.symbol = symbol 
        else:
            raise ValueError("The symbol must be in the default symbols list")
        if isinstance(score, float):
            self.score = score
        else:
            raise ValueError("Score must be a float value")
        if isinstance(computer, bool):
            self.computer = computer
        else: 
            raise ValueError("Computer must be a bool")

def main():
    while True:
        if not playing():
            break
    return 




def assign_symbols():
    symbol = None

    while (symbol not in SYMBOLS):
        symbol = input("Choose symbol: ").upper()

    return symbol

def create_player(id, symbol):
    new_player = player(id, symbol)
    return new_player

def ask(message):
    while True:
        ask = input(message)
        if ask.upper() in ["NO", "N"]:
            return False
        if ask.upper() in ["YES", "Y"]:
            return True


def playing():
    board_matrix = generate_board()

    display_board(board_matrix)
    

    #Assigning players
    p1 = create_player(1, assign_symbols())

    computer = ask("Would you like to play against a computer? ")

    print(f"computer: {computer}")

    p2 = create_player(2, SYMBOLS[(SYMBOLS.index(p1.symbol) + 1) % 2])

    p1_move = True
    players = [p1, p2]
    moves = 0

    while True:

        score = update_score(board_matrix, players)

        if score >= HAS_WON or score <= -HAS_WON:
            print("win")
            ask("Would you like to play again? ")
        elif draw(board_matrix):
            print("draw")
            ask("Would you like to play again? ")
        
        if computer and not p1_move:
            column = computer_play(board_matrix, players, moves)
            update = make_move(column, board_matrix, players, False)
        else:
            while True:
                column = choose_column()
                update = make_move(column, board_matrix, players, p1_move)
                if update != False:
                    break      
        
        moves += 1
        display_board(board_matrix)


        p1_move = not p1_move
             
            

if __name__ == "__main__":
    main()
