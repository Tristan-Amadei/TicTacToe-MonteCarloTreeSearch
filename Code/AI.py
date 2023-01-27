import numpy as np
from Board import Board
import time

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
                
    while len(board.moves) > nb_moves_beginning:
        board.undo_last_move()
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
    while len(board.moves) > nb_moves_beginning:
        board.undo_last_move()
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

'''
b = Board()
player = 1
while len(b.moves) < 9:
    play_minimax(b, player)
    b.display(True)
    time.sleep(4)
    
    if player == 1:
        player = -1
    else:
        player = 1 '''