import numpy as np
from Board import Board
import time

### Random Play ###

def play_random(board, player_AI, sleep_before=0):
    time.sleep(sleep_before)
    if board.gameState != 0 or len(board.moves) >= 9:
        return
    move_good = False
    while not move_good:
        i, j = np.random.randint(0, 3, 2)
        try:
            board.play(i, j, player_AI)
            move_good = True
        except:
            pass


### Minimax ###

def back_to_start_state(board, nb_moves_beginning):
    while len(board.moves) > nb_moves_beginning:
        board.undo_last_move()

def board_score(board):
    return 10 * board.gameState

def minimax_player1(board):    
    if len(board.moves) == 9:
        return board_score(board)
    
    nb_moves_beginning = len(board.moves)
    max_score = -10 #we'll try to maximize the score
    best_move = None
    for i in range(3):
        for j in range(3):
            if board.grid[i][j] == 0: #the square is free, we can play here
                try:
                    board.play(i, j, 1)                    
                    score = minimax_player2(board)[0]
                    board.undo_last_move()
                    if score >= max_score:
                        max_score = score
                        best_move = (i, j)
                except:
                    pass
                
    back_to_start_state(board, nb_moves_beginning)
    return max_score, best_move

def minimax_player2(board):
    if len(board.moves) == 9:
        return board_score(board)
    
    nb_moves_beginning = len(board.moves)
    min_score = +10 #we'll try to minimize the score
    best_move = None
    for i in range(3):
        for j in range(3):
            if board.grid[i][j] == 0: #the square is free, we can play here
                try:
                    board.play(i, j, -1)                    
                    score = minimax_player1(board)[0]
                    board.undo_last_move()
                    if score <= min_score:
                        min_score = score
                        best_move = (i, j)
                except:
                    pass
    back_to_start_state(board, nb_moves_beginning)
    return min_score, best_move

def play_minimax(board, player, sleep_before=0, search_on_copy=False):
    time.sleep(sleep_before)
    
    if board.gameState != 0 or len(board.moves) >= 9:
        return
    
    if search_on_copy:
        board_copy = board.copy() # we search the best move on a copy to avoid seeing some moves being played and removes on the gui
        board_to_search_on = board_copy
    else:
        board_to_search_on = board
        
    if player == 1:
        _, (i, j) = minimax_player1(board_to_search_on)
    else:
        _, (i, j) = minimax_player2(board_to_search_on)
        
    try:
        board.play(i, j, player)
    except:
        pass 


### Alpha-Beta ###

def alphaBeta_player1(board, alpha, beta):    
    if len(board.moves) == 9:
        return board_score(board)
    
    nb_moves_beginning = len(board.moves)
    best_move = None
    for i in range(3):
        for j in range(3):
            if board.grid[i][j] == 0: #the square is free, we can play here
                try:
                    board.play(i, j, 1)                    
                    score = alphaBeta_player2(board, alpha, beta)[0]
                    board.undo_last_move()
                    
                    if score > alpha:
                        alpha = score
                        best_move = (i, j)
                    
                    if score >= beta:
                        back_to_start_state(board, nb_moves_beginning)
                        return beta, best_move
                except:
                    pass
                
    back_to_start_state(board, nb_moves_beginning)
    return alpha, best_move

def alphaBeta_player2(board, alpha, beta):
    if len(board.moves) == 9:
        return board_score(board)
    
    nb_moves_beginning = len(board.moves)
    best_move = None
    for i in range(3):
        for j in range(3):
            if board.grid[i][j] == 0: #the square is free, we can play here
                try:
                    board.play(i, j, -1)                    
                    score = alphaBeta_player1(board, alpha, beta)[0]
                    board.undo_last_move()
                    
                    if score < beta:
                        beta = score
                        best_move = (i, j)
                        
                    if score <= alpha:
                        back_to_start_state(board, nb_moves_beginning)
                        return alpha, best_move
                except:
                    pass
                
    back_to_start_state(board, nb_moves_beginning)
    return beta, best_move

def play_alphaBeta(board, player, sleep_before=0, search_on_copy=False):
    time.sleep(sleep_before)
    
    if board.gameState != 0 or len(board.moves) >= 9:
        return
    
    if search_on_copy:
        board_copy = board.copy() # we search the best move on a copy to avoid seeing some moves being played and removes on the gui
        board_to_search_on = board_copy
    else:
        board_to_search_on = board
        
    if player == 1:
        _, (i, j) = alphaBeta_player1(board_to_search_on, -float('inf'), float('inf'))
    else:
        _, (i, j) = alphaBeta_player2(board_to_search_on, -float('inf'), float('inf'))
        
    try:
        board.play(i, j, player)
    except:
        pass 