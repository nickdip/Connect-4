from helpers import *

class board():

    """state should be -1 if unavailable, 0 if empty but available or 1 if avaialble
    p1_win/p2_win default is 0, meaning cannot win yet, +2 if it's a win or a +1 if less likely win (which means in the column, 
    there are wins lower down in that column which are more likely)"""
    def __init__(self, id, p1_win, p2_win, state = None, display = EMPTY):
        if isinstance(id, int):
            self.id = id 
            
        else:
            raise ValueError("id and can_Win must all be an integer")
        if isinstance(state, int):
            if state >= -1 or state <= 1:
                self.state = state 
            else:
                raise ValueError ("This value msust be either 0, -1 or 1")
        if isinstance(display, str):
            if display in SYMBOLS or display == EMPTY:
                self.display = display

            else:
                raise ValueError("The display can only be changed to one of the assigned symbols")
        if all(isinstance(p, int) for p in [p1_win, p2_win]):
                self.p1_win = p1_win
                self.p2_win = p2_win   
        else:
            raise ValueError("player wins must be an integer")
        

    def is_winning(self, symbol):
        return symbol in self.can_win


def generate_board(): 
        board_matrix = []
        id_number = 1
        for i in range(WIDTH):
            column_list = []
            for j in range(HEIGHT):
                slot = board(id_number, 0, 0)
                if j == 0:
                    slot.state = 1
                else:
                    slot.state = 0
                column_list += [slot]
                id_number += 1
            board_matrix += [column_list]

        return board_matrix

def display_board(board_matrix):
    print("1 2 3 4 5 6 7")
    for i in range(HEIGHT-1, -1, -1):
        for j in range(WIDTH):
                print(board_matrix[j][i].display + " ", end ="")
        print()
    print()
    print()

board_matrix = generate_board()
