from helpers import *
from lines import *


#This function counts the number of slots in a connection that has a particular display attr     
def count_display(connection_list, display_symbol, frequency):
    count = 0
    for c in connection_list:
        if sum(getattr(slot, "display") == display_symbol for slot in c) == frequency:
            count += 1
    return count
        

def player_wins(current_player_values, opposing_player_values, player_obj, p1):
    if p1:
        if player_obj.id == 1:
            return current_player_values
        else:
            return opposing_player_values
    else:
        if player_obj.id == 1:
            return opposing_player_values
        else:
            return current_player_values


"""This function will search for particular 'lines' on the board of a particular length (see lines.y for 
for connectiion function). The name is currently misleading - you can search for lines greater than 4!


player_wins is used here to help identify whether we want to allow p1 wins or p2 wins"""
def four_combinations(all_lines, player):
    score = 0
    connection_list = connections(all_lines,
                                [-1,0, 1], #allowed states
                                [player.symbol, "*", EMPTY], #allowed symbols
                                player_wins([-1, 0, 1, 2], [-1,0, 1, 2], player, True), #allowed p1 wins
                                player_wins([-1, 0, 1, 2], [-1,0, 1, 2], player, False), #alowed p2 wins
                                4)
    
    score += count_display(connection_list, player.symbol, 1) * LINE_SCORE1
    score += count_display(connection_list, player.symbol, 2) * LINE_SCORE1
    score += count_display(connection_list, player.symbol, 3) * LINE_SCORE2

    connection_list = connections(all_lines, 
                                [-1,1], 
                                [player.symbol, EMPTY],
                                player_wins([-1, 0, 1, 2], [-1,0,1,2], player, True),
                                player_wins([-1, 0, 1, 2], [-1,0,1,2], player, False),
                                5) 

    #This checks whether there is a forced win
    display_connection = show_attr(connection_list, "display")
    temp_list = []
    for connection in display_connection:
        if connection[0] == EMPTY  and connection[-1] == EMPTY and connection.count(player.symbol) > 1:
            temp_list += [connection]
    connection_list = temp_list

    if len(connection_list) > 0:
        score += FORCE_WIN
    
    return score




def exploring_next_move(all_lines, players, player):

    opposing_player = players[(players.index(player) + 1) % 2]

    score = 0
     #Looking for one or more lines with available win and 3 counters

    connection_list = connections(all_lines, 
                                   [-1,1], 
                                   [player.symbol, EMPTY],
                                   player_wins([-1, 0, 1, 2, "*"], [-1,0,1,2], player, True),
                                   player_wins([-1, 0, 1, 2, "*"], [-1,0,1,2], player, False),
                                    4) 
     
    win_freq = count_display(connection_list, player.symbol, 3)
    if win_freq == 1:
        score += WIN


    attr_options = ["p1_win", "p2_win"]
    for lines in all_lines["vertical"]:
        for index in range(len(lines) - 1):
            if getattr(lines[index], attr_options[players.index(player)]) == 2 and getattr(lines[index + 1], attr_options[players.index(player)]) == 2:
                score += FORCE_WIN 


    return score

def update_score(board_matrix, players):

    all_lines = combined_lines(board_matrix)

    score = 0
        
    for key in all_lines: 
        for lines in all_lines[key]: 
            if checking_win(lines, players[0].symbol):
                return HAS_WON
            if checking_win(lines, players[1].symbol):
                return -HAS_WON
            
    score += four_combinations(all_lines, players[0]) - four_combinations(all_lines, players[1])

    score += exploring_next_move(all_lines, players, players[0]) - exploring_next_move(all_lines, players, players[1]) 
    
    return score


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

def draw(board_matrix):
    count = 0
    for column in board_matrix:
        if column[HEIGHT - 1].display in SYMBOLS:
            count += 1
    return count == WIDTH
