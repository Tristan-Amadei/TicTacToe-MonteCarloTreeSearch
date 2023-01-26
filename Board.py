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
                return
            if self.playerWins_column(i, j, player):
                self.gameState = player
                return
            if self.playerWins_diag(player):
                self.gameState = player

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
            return True
        return self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == player

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


b = Board()

b.play(0, 0, 1)
b.display(True)
b.play(1, 1, -1)
b.display(True)
b.play(1, 0, 1)
b.display(True)
b.play(2, 2, -1)
b.display(True)
print(b.gameState)
print(b.nbMovesPlayed)
b.play(2, 0, 1)
b.display()
print(b.gameState)
print(b.nbMovesPlayed)
b.play(0, 1, -1)