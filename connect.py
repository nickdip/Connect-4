from board import *
from helpers import *
from copy import deepcopy
from evaluating import *
from lines import *


def choose_column():
    while True:
        column = input("Choose column: ")
        if column.isdigit():
            column = int(column)
            if column in COLUMNS:
                return column - 1

def make_move(column, board_matrix, players, p1_move):

    if p1_move:
        current_player = players[0] 
    
    else:
        current_player = players[1]
    
    opposing_player_index = (players.index(current_player) + 1) % 2

    if not available(column, board_matrix):
        return False
    
    change = False
    for slot in board_matrix[column]:
        if change: #Changing the slot above
            setattr(slot, "state", 1)
            break

        if getattr(slot, "state") == 1:
            setattr(slot, "state", -1)
            setattr(slot, "display", current_player.symbol)
            setattr(slot, PLAYER_WINS[opposing_player_index], -1)
            change = True

    update_board(board_matrix, [players[0].symbol, players[1].symbol])
    

"""Board upates as true if there is a win or draw if false """
def update_board(board_matrix, players):

    #Checking for win
    all_lines = combined_lines(board_matrix)

    """checking for slots that are a potential win"""
    for key in all_lines: 
        for lines in all_lines[key]: 
            for slot in lines:

            #temporarily change the slot to both player symbols to see if this is a winnning slot

                for player in players:
                    if getattr(slot, "state") != -1:
                        setattr(slot, "display", player)
                        if checking_win(lines, player):
                            setattr(slot, PLAYER_WINS[players.index(player)], 2)
                        setattr(slot, "display", EMPTY)



    #Changing any unlikely wins in a vertical colum
    for vertical_lines in board_matrix:
        
        for player_index, player in enumerate(players):

            saved_index = None

            for slot_index, slot in enumerate(vertical_lines):
              
            
                if ( saved_index == None or slot_index == saved_index + 1 ) and getattr(slot, PLAYER_WINS[player_index]) == 2:
                    saved_index = slot_index

                elif saved_index != None:

                    if slot_index % 2  == saved_index % 2 and  getattr(slot, PLAYER_WINS[player_index]) == 2:
                        setattr(slot, PLAYER_WINS[player_index], 1)
                        

                    if slot_index % 2 != saved_index % 2 and getattr(slot, PLAYER_WINS[(player_index + 1) % 2]) == 2:
                        setattr(slot, PLAYER_WINS[(player_index + 1) % 2], 1)
    return True


def checking_win(lines, symbol):

    count = 1
    element_checked = None
    for slot in lines:
        
        display_attr = getattr(slot, "display") 

        if display_attr == symbol:

            if display_attr == element_checked:
                count += 1
                if count >= 4:
                    return True
        if display_attr != element_checked:
            count = 1
            element_checked = slot.display
    return False


#returns false is a column is full
def available(column, board_matrix):
    if board_matrix[column][HEIGHT - 1].display in SYMBOLS:
        return False
    return True


"""prints the board with the attributes of each object, for testing purposes only"""

def test_board(board_matrix):
    for i in range(1,8):
        print(" "*10 + str(i) + " "*13, end="")
    print() 
    for i in range(HEIGHT-1, -1, -1):
        for j in range(WIDTH):
            print(f"({board_matrix[j][i].state}, {board_matrix[j][i].display}, [{board_matrix[j][i].p1_win}, {board_matrix[j][i].p2_win}])", end = "")
        print()
    print()
    print()

"""This will undo the last move for a particular column"""
def undo_move(column, board_matrix, players):

    for index in range(len(board_matrix[column]) - 1, -1, -1):
        if getattr(board_matrix[column][index], "display") in SYMBOLS:
            player_symbol = getattr(board_matrix[column][index], "display")
            setattr(board_matrix[column][index], "state", 1)
            setattr(board_matrix[column][index], "display", player_symbol)
            setattr(board_matrix[column][index], PLAYER_WINS[0], 0)
            setattr(board_matrix[column][index], PLAYER_WINS[1], 0)
            if index != len(board_matrix[column]) - 1:
                setattr(board_matrix[column][index + 1], "state", 0)
            break
        
    for column in board_matrix:
        for slot in column:
            for player in players:
                setattr(slot, PLAYER_WINS[players.index(player)], 0)

    update_board(board_matrix, players)
    
