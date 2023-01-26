import numpy as np
from Board import Board
import time

def play_random(board, player_AI, sleep_before=0):
    time.sleep(sleep_before)
    if board.gameState != 0 or board.nbMovesPlayed == 9:
        return
    move_good = False
    while not move_good:
        i, j = np.random.randint(0, 3, 2)
        try:
            board.play(i, j, player_AI)
            move_good = True
        except:
            pass
