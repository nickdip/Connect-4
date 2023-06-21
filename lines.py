from helpers import *

"""Returns lists of all the possible lines that can be created"""
def combined_lines(board_matrix):
    return {"pos diagonal": pos_diagonals(board_matrix),
            "neg diagonal": neg_diagonals(board_matrix),
            "vertical": board_matrix,
            "horizontal": horizontal(board_matrix)
            }

def pos_diagonals(board_matrix):
    pos_diagonals = []

    for row in range(WIDTH + HEIGHT - 6 - 1):
        diagonal = []
        if row < HEIGHT - 3:
            step_x = 0
            step_y = HEIGHT - 4 - row
        else:
            step_x = row - HEIGHT + 4
            step_y = 0

        while step_y < HEIGHT and step_x < WIDTH:
            diagonal += [board_matrix[step_x][step_y]]
            step_x += 1
            step_y += 1
        
        pos_diagonals += [diagonal]
    return pos_diagonals 


def neg_diagonals(board_matrix):
    neg_diagonals = []

    for row in range(WIDTH + HEIGHT - 6 - 1):
        diagonal = []
        if row < HEIGHT - 3:
            step_x = 0
            step_y = HEIGHT - 3 + row
        else:
            step_x = row - HEIGHT + 4
            step_y = HEIGHT - 1

        while step_y >= 0 and step_x < WIDTH:
            diagonal += [board_matrix[step_x][step_y]]
            step_x += 1
            step_y -= 1
        
        neg_diagonals += [diagonal]

    return neg_diagonals 

def horizontal(board_matrix):
    horizontal = [] 
    for index in range(HEIGHT):
        line = []
        for column in board_matrix:
            line += [column[index]]
        horizontal += [line]
    return horizontal 

""""This function allows us to generate combinations of any length on the board

Example:

    possible_lines = connections(all_lines, 
                                 [-1, 0, 1], #allowed_states
                                 [SYMBOLS[0], "*", SYMBOLS[1], "*", EMPTY],  #allowed-DISPLAYS
                                 [-1, 0, 1, 2], #allowed-wins
                                 [-1, 0, 1, 2], #allowed-wins
                                 4)

                                
The * indicates that the previous value MUST be included. 
"""


def connections(all_lines, allowed_states, allowed_displays, allowed_p1win, allowed_p2win, length):

    def must_inc_check(connection_list, must_include_dict_values, message):     
        new_connection_list = []

        for line in connection_list:

            include = []

            for i in range(len(must_include_dict_values)):
                include += [False] 


            for i, must_include in enumerate(must_include_dict_values):
                if any(getattr(slot, message) == must_include for slot in line):
                    include[i] = True

            if all(include[i] == True for i in range(len(include))):

                new_connection_list += [line]

        return new_connection_list
  
    def check_slot(slot, allowed_dict): #Checks whether each attribute is in the slot and any essential values are there 
        if all(getattr(slot, list(allowed_attr.keys())[0]) in allowed_dict[index][list(allowed_attr.keys())[0]] 
               for index, allowed_attr in enumerate(allowed_dict)):
                    return True

    def generate(line, allowed_dict, length, must_include_dict):
        connection_list = []
        
        for slot_index, slot in enumerate(line):
            connection = []
            step = 0
            if check_slot(slot, allowed_dict):
                while step < length and slot_index + step < len(line):
                    if check_slot(line[slot_index + step], allowed_dict):
                        connection += [line[slot_index + step]]
                        step += 1
                    else: 
                        break
                    if len(connection) == length:
                        connection_list += [connection]

        if len(connection_list) > 0:  
            for key in list(must_include_dict.keys()): #Delete any lists that don't include items from must_include_dict
                connection_list = must_inc_check(connection_list, must_include_dict[key], key)

        
        return connection_list
    
    def must_include(must_include_dict, allowed_attr, message):
        must_include_values = []
        for index, item in enumerate(allowed_attr):
            if item == "*":
                
                must_include_values += [allowed_attr[index - 1]]
                must_include_dict[message] = must_include_values
                del allowed_attr[index]
        return allowed_attr
        
    """This part creates a dictionary of attribute values that must be included"""
    must_include_dict = {}
    allowed_states =  {"state": must_include(must_include_dict, allowed_states, "state")}
    allowed_displays = {"display": must_include(must_include_dict, allowed_displays, "display")}
    allowed_p1win  = {"p1_win": must_include(must_include_dict, allowed_p1win, "p1_win")}
    allowed_p2win  = {"p2_win": must_include(must_include_dict, allowed_p2win, "p2_win")}

    allowed_dict = [allowed_states, allowed_displays, allowed_p1win, allowed_p2win]

    

        
    possible_lines = []
    count = 0
    
    for key in all_lines: 
        for line in all_lines[key]: 
            possible_lines += generate(line, allowed_dict, length, must_include_dict)
    
    return possible_lines


#This shows the line objects by a given attribute, for testing purposes
def show_attr(possible_lines, attr):

    attr_list = ["display", "state", "can_win", "id"]
    
    if attr not in attr_list:
        return False

    poss_lines = []
    for lines in possible_lines:
        line = []
        for slot in lines:
            line += [getattr(slot, attr)]
        poss_lines += [line] 

    return poss_lines

