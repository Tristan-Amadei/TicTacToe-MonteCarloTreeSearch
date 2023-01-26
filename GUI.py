import pygame
from Board import Board, direction
from AI import *
from threading import Thread

pygame.font.init()
pygame.init()

def player_color(player):
    color_blood_red = (136, 8, 8)
    color_blue = (60, 60, 190)
    if player == 1:
        return color_blood_red
    elif player == -1:
        return color_blue

def winning_color(gameState):
    color_red = (255, 0, 0)
    color_blue = (0, 0, 255)
    if gameState == 1:
        return color_red
    elif gameState == -1:
        return color_blue
    return (0, 0, 0)

def draw_cell(win, i, j, board, width, height, player_string):
    fnt = pygame.font.SysFont("comicsans", 120)
    gap = width / 3
    x = j * gap
    y = i * gap

    if board.grid[i][j] == 0:
        return
    
    text = fnt.render(board.display_player_name(board.grid[i][j]), 
                                                1, player_color(board.grid[i][j]))
    win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

def draw_selected_cell(win, selected, width):
    if selected[0] == -1 or selected[1] == -1:
        #no square is currently selected
        return
    
    gap = width / 3
    x = selected[1] * gap
    y = selected[0] * gap
    pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

def draw(win, board, width, height, player_string):
    gap = width / 3
    for i in range(3+1):
        thick = 4
        pygame.draw.line(win, (0,0,0), (0, i*gap), (width, i*gap), thick)
        pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, gap*3), thick)

    for i in range(3):
        for j in range(3):
            draw_cell(win, i, j, board, width, height, player_string)

def redraw_window(win, board, width, height, player, player_string, selected):
    win.fill((255,255,255))
    # Draw player
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Player: ", 1, (0,0,0))
    win.blit(text, (10, height-text.get_height()-12.5))
    text_player = fnt.render(player_string, 1, player_color(player))
    win.blit(text_player, (text.get_width()+10, height-text.get_height()-10))

    # Draw grid and board
    draw(win, board, width, height, player_string)

    # Draw square around the selected cell
    draw_selected_cell(win, selected, width)

    #Draw lines to show the winner
    draw_winner(win, board, width)

def click_square(mouse_pos, selected, width, height, board, player):
    gap = width / 3
    if mouse_pos[0] < width and mouse_pos[1] < height:
        x = int(mouse_pos[0] // gap)
        y = int(mouse_pos[1] // gap)
        if selected[0] == y and selected[1] == x:
            #the square was already selected, selecting it again means we want to play on there
            try:
                board.play(y, x, player)
                selected[0] = -1
                selected[1] = -1
                return True
            except:
                selected[0] = -1
                selected[1] = -1
                return False
        else:
            selected[0] = y
            selected[1] = x
            return False

def draw_winner(win, board, width):
    gap = width / 3
    if board.winningMove != None:
        (i, j), dir = board.winningMove
        color = winning_color(board.gameState)
        if dir == direction.ROW:
            pygame.draw.line(win, color, (gap/2, i*gap + gap/2), 
                                           (width - gap / 2, i*gap + gap / 2), 6)
        if dir == direction.COL:
            pygame.draw.line(win, color, (j*gap + gap/2, gap/2), 
                                           (j*gap + gap / 2, width - gap / 2), 6)
        if dir == direction.DIAG_TOP_BOTTOM:
            pygame.draw.line(win, color, (gap/2, gap/2), 
                                           (width - gap / 2, width - gap / 2), 6)
        if dir == direction.DIAG_BOTTOM_TOP:
            pygame.draw.line(win, color, (width - gap/2, gap/2), 
                                           (gap / 2, width - gap / 2), 6)



def main():
    screenInfo = pygame.display.Info()
    width = 0.4*screenInfo.current_w
    height = 0.8*screenInfo.current_h
    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Tic-Tac-Toe")

    run = True
    boardInitialized = False

    while run:
        if not boardInitialized:
            board = Board()

            player = 1
            player_string = "X" if player == 1 else "O"
            opponent = -1

            selected = [-1, -1]
            boardInitialized = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                move_was_played = click_square(mouse_pos, selected, width, height, board, player)
                if move_was_played:
                    thread = Thread(target=play_random, args=(board, opponent, 0.5))
                    thread.start()               

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window(win, board, width, height, player, player_string, selected)
        pygame.display.update()

main()