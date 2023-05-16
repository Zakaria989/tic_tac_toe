import numpy as np
import pygame
import time


pygame.init()
running = True
font = pygame.font.SysFont("rekha", 90, bold=True)
# start_game = input(f"Do you want to play, type y og n: ")

# while start_game != 'y' or 'n':
#     print(start_game)
#     if start_game == 'y':
#         running = True
#         break
#     elif start_game == 'n':
#         break
#     else:
#         start_game = input(f"Do you want to play, type y og n: ")

def player_checker(player_current):
    player_1 = "O"
    player_2 = "X"
    if player_current == player_1:
        player_current = player_2
    elif player_current == player_2:
        player_current = player_1
    return player_current

def is_play_in_moves(play, moves):
    row,col,x = play
    for move in moves:
        if move[0] == row and move[1] == col:
            return True

    return False

def check_winning_condition(moves):
    winning_moves = [
        [(0, 0, "X"), (0, 1, "X"), (0, 2, "X")],
        [(1, 0, "X"), (1, 1, "X"), (1, 2, "X")],
        [(2, 0, "X"), (2, 1, "X"), (2, 2, "X")],
        [(0, 0, "X"), (1, 0, "X"), (2, 0, "X")],
        [(0, 1, "X"), (1, 1, "X"), (2, 1, "X")],
        [(0, 2, "X"), (1, 2, "X"), (2, 2, "X")],
        [(0, 0, "X"), (1, 1, "X"), (2, 2, "X")],
        [(0, 2, "X"), (1, 1, "X"), (2, 0, "X")],
        [(0, 0, "O"), (0, 1, "O"), (0, 2, "O")],
        [(1, 0, "O"), (1, 1, "O"), (1, 2, "O")],
        [(2, 0, "O"), (2, 1, "O"), (2, 2, "O")],
        [(0, 0, "O"), (1, 0, "O"), (2, 0, "O")],
        [(0, 1, "O"), (1, 1, "O"), (2, 1, "O")],
        [(0, 2, "O"), (1, 2, "O"), (2, 2, "O")],
        [(0, 0, "O"), (1, 1, "O"), (2, 2, "O")],
        [(0, 2, "O"), (1, 1, "O"), (2, 0, "O")]
    ]
    for combination in winning_moves:
        if all(move in moves for move in combination):
            return True
    return False

def type_winner_to_screen(moves):
    x,y,player_won = moves[-1]
    text = f"{player_won} won!"
    text_surface = font.render(text,True,(0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text_surface,text_rect)
    pygame.display.flip()




# Drawing the board, and redrawing it after moves
def draw_board(blocks, moves):
    screen.fill("white")
    line_width = 5
    for block_rect in blocks:
        pygame.draw.rect(screen, 'black', block_rect, line_width)
    

    for move in moves:
        row, col, player = move
        x = blocks[row * 3 + col].x + block_size[0] / 2
        y = blocks[row * 3 + col].y + block_size[1] / 2
        
        if player == "O":
            radius = (min(block_size[0], block_size[1]) / 10)*1.9
            pygame.draw.circle(screen, 'black', (x, y), radius, line_width)
        elif player == "X":
            line_length = min(block_size[0], block_size[1]) / 6
            pygame.draw.line(screen, 'black', (x - line_length, y - line_length), (x + line_length, y + line_length), line_width)
            pygame.draw.line(screen, 'black', (x - line_length, y + line_length), (x + line_length, y - line_length), line_width)

    pygame.display.flip()

screen = pygame.display.set_mode((460, 360))
clock = pygame.time.Clock()
dt = 0
block_size = (screen.get_width() / 3, screen.get_height() / 3)
blocks = [pygame.Rect(col * block_size[0], row * block_size[1], *block_size) for row in range(3) for col in range(3)]

moves = []
player_current = "O"
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (int(mouse_pos[0]), int(mouse_pos[1]))  # Round the mouse position
            for i, block_rect in enumerate(blocks):
                if block_rect.collidepoint(mouse_pos) and game_over == False:
                    row = i // 3
                    col = i % 3
                    move = (row, col, player_current)
                    if not is_play_in_moves(move, moves):  # Check if move is valid
                        moves.append(move)
                        player_current = player_checker(player_current)
                    if len(moves) >= 5:  # Check winning condition after 5 moves
                        if check_winning_condition(moves):
                            x,y,player_won = moves[-1]
                            game_over = True
                            type_winner_to_screen(moves)
                            time.sleep(5)  # Delay for 2 seconds
                    if len(moves) == 9:
                        if check_winning_condition(moves):
                            type_winner_to_screen(moves)
                            game_over = True
                            
                        else:
                            type_winner_to_screen(moves)
                            game_over = True
                                                    
    draw_board(blocks, moves)
    dt = clock.tick(60) / 1000
pygame.quit()