from connect import *
import random

def computer_play(board_matrix, players, moves):
    if moves < 2:
        return 3
    score_list = {} 
    score = 0
    maximiser = True
    alpha = -1000000
    beta = 1000000
    min_score = beta
    for column in range(WIDTH):
        if available(column, board_matrix):
            make_move(column, board_matrix, players, False)
            if update_score(board_matrix, players) <= -HAS_WON:
                undo_move(column, board_matrix, players)
                return column 
            score = pruning(board_matrix, 0, alpha, beta, players, maximiser)
            score_list[column] = score
            print(f"score: {score}")
            print(f"min score: {min_score}")
            if score <= min_score:
                print("HI")
                column_choice = column
                min_score = score

            #score_list[column] = pruning(board_matrix, 0, -1000000, 1000000, players, maximiser)
            undo_move(column, board_matrix, players)

    print(score_list)
    print(column_choice)
    return column_choice

    """Randomness removed due to bug!"""
    #possible_columns = []
    #for column, score in score_list.items():
    #    if score == min(list(score_list.values())):
    #        possible_columns += [column]
    
    #return random.choice(possible_columns)


def pruning(board_matrix, depth, alpha, beta, players, maximiser):
    
    score = update_score(board_matrix, players)
    
    if score == "draw":
        return 0
    
    if depth == 3: #end of check (minimiser)
        return score
        

    if maximiser: #player1
        if score >= HAS_WON:
            return score
        for column in range(WIDTH):
            if available(column, board_matrix):        
                make_move(column, board_matrix, players, True)
                best = pruning(board_matrix, depth + 1, alpha, beta, players, False)
                if best > alpha:
                    alpha = best
                undo_move(column, board_matrix, players)
                if alpha >= beta:
                    break
        return alpha
    
    else:
        if score <= -HAS_WON:
            return score
        for column in range(WIDTH):
            if available(column, board_matrix):  
                make_move(column, board_matrix, players, False)
                best = pruning(board_matrix , depth + 1, alpha, beta, players, True)
                if best < beta:
                    beta = best
                undo_move(column, board_matrix, players)
                if alpha >= beta:
                    break
        return beta 