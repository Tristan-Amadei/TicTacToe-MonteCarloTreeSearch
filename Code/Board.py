from enum import Enum

class direction(Enum):
    ROW = 1
    COL = 2
    DIAG_TOP_BOTTOM = 3
    DIAG_BOTTOM_TOP = 4

class Board:
    ##### Players #####
    ## 1 = player X
    ## -1 = player O

    ##### Game State #####
    ## 0 and 9 moves played: draw
    ## -1: player O wins the game
    ## 1: player X wins the game


    def __init__(self):
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.lastPlayerToPlay = 0
        self.gameState = 0
        self.nbMovesPlayed = 0
        self.winningMove = None

    def display_cell(self, i, j):
        if self.grid[i][j] == 0:
            print('   ', end = '')
        elif self.grid[i][j] == 1:
            print(' X ', end = '')
        else:
            print(' O ', end = '')

    def display(self, addSpace=False):
        for i in range(3):
            for j in range(3):
                self.display_cell(i, j)
                if j < 2:
                    print('|', end='')
                else:
                    print()
            if i < 2:
                print('-----------')
        if addSpace:
            print()

    def display_player_name(self, player):
        if player == 1:
            return "X"
        return "O"

    def updateGameState(self, i, j, player):
        #i, j stand for the coordinates of the last move played 
        #player is the player that played the last move
        if self.nbMovesPlayed == 9 or self.gameState != 0:
            pass
        else:
            #check if the player has won on the row
            if self.playerWins_row(i, j, player):
                self.gameState = player
                self.winningMove = ((i, j), direction.ROW) 
                return
            if self.playerWins_column(i, j, player):
                self.gameState = player
                self.winningMove = ((i, j), direction.COL) 
                return
            
            won_on_diagonal = self.playerWins_diag(player)
            if won_on_diagonal[0]:
                self.gameState = player
                if won_on_diagonal[1] == 1:
                    dir = direction.DIAG_TOP_BOTTOM
                else:
                    dir = direction.DIAG_BOTTOM_TOP
                self.winningMove = ((i, j), dir)

    def playerWins_row(self, i, j, player):
        if j == 0:
            return self.grid[i][j+1] == self.grid[i][j+2] == player
        if j == 1:
            return self.grid[i][j-1] == self.grid[i][j+1] == player
        return self.grid[i][j-2] == self.grid[i][j-1] == player

    def playerWins_column(self, i, j, player):
        if i == 0:
            return self.grid[i+1][j] == self.grid[i+2][j] == player
        if i == 1:
            return self.grid[i-1][j] == self.grid[i+1][j] == player
        return self.grid[i-1][j] == self.grid[i-2][j] == player

    def playerWins_diag(self, player):
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == player:
            #diagonal from top right corner to bottom left corner
            return (True, 1)
        return (self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == player, 2)

    def play(self, i, j, player):
        if self.gameState != 0 or self.nbMovesPlayed >= 9:
            text = "The game is a draw." if self.gameState == 0 else f"Player {self.display_player_name(self.gameState)} has won."
            raise Exception(text)
        elif self.grid[i][j] == 0:
            if self.lastPlayerToPlay == player:
                players_turn = 1 if player == -1 else -1
                raise Exception(f"It's player {self.display_player_name(players_turn)}'s turn to play.")
            else:
                self.grid[i][j] = player
                self.lastPlayerToPlay = player
                self.nbMovesPlayed += 1
                self.updateGameState(i, j, player)
        else:
            raise Exception(f"Cell [{i}, {j}] is not empty.")