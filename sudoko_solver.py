# Sudoku solver and visualiser using pygame

import pygame

pygame.init()

# Main window
SQUARES = 9
SPACING = 50
WIDTH = SPACING * SQUARES
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Sudoko by Rory")
font = pygame.font.SysFont("Courier", int(SPACING))
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WIGHT = (255, 255, 255)
win.fill(WIGHT)

s_board = [[5, 3, 0, 0, 7, 0, 9, 0, 0],
           [6, 0, 0, 1, 9, 5, 0, 0, 0],
           [0, 9, 8, 3, 4, 0, 0, 6, 7],
           [8, 0, 9, 0, 6, 0, 4, 0, 3],
           [4, 0, 0, 8, 0, 3, 0, 0, 1],
           [7, 0, 3, 0, 2, 0, 0, 0, 6],
           [0, 6, 1, 0, 0, 0, 2, 8, 0],
           [0, 0, 0, 4, 1, 9, 0, 0, 5],
           [0, 4, 0, 2, 8, 0, 0, 7, 9]]

p_board = [[5, 3, 0, 0, 7, 0, 9, 0, 0],
           [6, 0, 0, 1, 9, 5, 0, 0, 0],
           [0, 9, 8, 3, 4, 0, 0, 6, 7],
           [8, 0, 9, 0, 6, 0, 4, 0, 3],
           [4, 0, 0, 8, 0, 3, 0, 0, 1],
           [7, 0, 3, 0, 2, 0, 0, 0, 6],
           [0, 6, 1, 0, 0, 0, 2, 8, 0],
           [0, 0, 0, 4, 1, 9, 0, 0, 5],
           [0, 4, 0, 2, 8, 0, 0, 7, 9]]

selected_box = []
empty_squares = []


# Functions - pygame
def redraw_game_window(board):
    draw_grid()
    draw_numbers(board)
    pygame.display.update()


def draw_grid():
    for line in range(0, WIDTH, SPACING):
        if line % 3 == 0:
            pygame.draw.line(win, BLACK, (line, 0), (line, WIDTH), 3)
            pygame.draw.line(win, BLACK, (0, line), (WIDTH, line), 3)
        else:
            pygame.draw.line(win, BLACK, (line, 0), (line, WIDTH))
            pygame.draw.line(win, BLACK, (0, line), (WIDTH, line))


def draw_numbers(board, black=True):
    row_count = 0
    for r in board:
        col_count = 0
        for num in r:
            if num != 0:
                if black:
                    label = font.render("{}".format(num), 1, BLACK)
                else:
                    label = font.render("{}".format(num), 1, GREY)
                win.blit(label, ((SPACING * col_count) + 10, (SPACING * row_count)))
            col_count += 1
        row_count += 1


def select_box(x, y):
    global selected_box
    selected_box = []
    selected_box = [x//SPACING, y//SPACING]
    win.fill(WIGHT)
    pygame.draw.rect(win, RED, ((SPACING * (x // SPACING)), (SPACING * (y // SPACING)), SPACING, SPACING))
    pygame.draw.rect(win, WIGHT,
                     (((SPACING * (x // SPACING)) + 3), ((SPACING * (y // SPACING)) + 3), SPACING - 6, SPACING - 6))
    draw_numbers(p_board, False)
    redraw_game_window(s_board)


def draw_player_number(n):
    if is_valid_number(p_board, n, selected_box[1], selected_box[0]):
        p_board[selected_box[1]][selected_box[0]] = n
        draw_numbers(p_board, False)


def delete_number(x, y):
    if s_board[x][y] == 0:
        p_board[x][y] = 0
    win.fill(WIGHT)
    draw_numbers(p_board, False)
    redraw_game_window(s_board)


def wait(t):
    global run
    i = 0
    while i < t:
        pygame.time.wait(1)
        i += 1
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                run = False
                pygame.quit()


# Functions - sudoku
def find_empty_squares(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                empty_squares.append([r, c])


def is_valid_number(board, number, row, col):
    # Checking for number in row
    for c in range(9):
        if c == col:
            pass
        elif board[row][c] == number:
            return False
    # Checking for number in col
    for r in range(9):
        if r == row:
            pass
        elif board[r][col] == number:
            return False
    # Checking boxes along top
    if 0 <= row <= 2:
        if 0 <= col <= 2:
            for r in range(3):
                for c in range(3):
                    if board[r][c] == number:
                        return False
        elif 3 <= col <= 5:
            for r in range(3):
                for c in range(3, 6):
                    if board[r][c] == number:
                        return False
        elif 6 <= col <= 8:
            for r in range(3):
                for c in range(6, 9):
                    if board[r][c] == number:
                        return False
    # Checking boxes along middle
    elif 3 <= row <= 5:
        if 0 <= col <= 2:
            for r in range(3, 6):
                for c in range(3):
                    if board[r][c] == number:
                        return False
        elif 3 <= col <= 5:
            for r in range(3, 6):
                for c in range(3, 6):
                    if board[r][c] == number:
                        return False
        elif 6 <= col <= 8:
            for r in range(3, 6):
                for c in range(6, 9):
                    if board[r][c] == number:
                        return False
    # Checking boxes along bottom
    elif 6 <= row <= 8:
        if 0 <= col <= 2:
            for r in range(6, 9):
                for c in range(3):
                    if board[r][c] == number:
                        return False
        elif 3 <= col <= 5:
            for r in range(6, 9):
                for c in range(3, 6):
                    if board[r][c] == number:
                        return False
        elif 6 <= col <= 8:
            for r in range(6, 9):
                for c in range(6, 9):
                    if board[r][c] == number:
                        return False
    return True


def board_full(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return False
    return True


def board_solved(board, square):
    global run
    if board_full(board):
        return True
    row = empty_squares[square][0]
    col = empty_squares[square][1]
    square += 1
    for n in range(1, 10):
        if is_valid_number(board, n, row, col):
            board[row][col] = n
            win.fill(WIGHT)
            pygame.draw.rect(win, YELLOW, ((SPACING * col), (SPACING * row), SPACING, SPACING))
            redraw_game_window(board)
            wait(50)
            if board_solved(board, square):
                return True
        board[row][col] = 0
    return False


def solve_board(board):
    find_empty_squares(board)
    if board_solved(board, 0):
        return board
    else:
        return board


# Main loop setup
run = True
clock = pygame.time.Clock()

pygame.font.get_fonts()

# Main loop
while run:

    if board_full(s_board):
        p_board = s_board

    draw_numbers(p_board, False)
    redraw_game_window(s_board)

    # Check for event - quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            select_box(event.pos[0], event.pos[1])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        solve_board(s_board)

    if keys[pygame.K_BACKSPACE]:
        delete_number(selected_box[1], selected_box[0])

    if keys[pygame.K_1]:
        draw_player_number(1)
    elif keys[pygame.K_2]:
        draw_player_number(2)
    elif keys[pygame.K_3]:
        draw_player_number(3)
    elif keys[pygame.K_4]:
        draw_player_number(4)
    elif keys[pygame.K_5]:
        draw_player_number(5)
    elif keys[pygame.K_6]:
        draw_player_number(6)
    elif keys[pygame.K_7]:
        draw_player_number(7)
    elif keys[pygame.K_8]:
        draw_player_number(8)
    elif keys[pygame.K_9]:
        draw_player_number(9)

pygame.quit()
