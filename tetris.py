import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Shapes and their respective colors
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1],
     [0, 1, 0]],     # T
    [[1, 1, 1],
     [1, 0, 0]],     # L
    [[1, 1, 1],
     [0, 0, 1]],     # J
    [[0, 1, 1],
     [1, 1, 0]],     # S
    [[1, 1, 0],
     [0, 1, 1]],     # Z
    [[1, 1],
     [1, 1]]         # O
]

# Different colors for each shape
COLORS = [(255, 0, 0),    # Red
          (0, 255, 0),    # Green
          (0, 0, 255),    # Blue
          (255, 255, 0),  # Yellow
          (255, 0, 255),  # Magenta
          (0, 255, 255),  # Cyan
          (255, 165, 0)]  # Orange

# Define the Tetris board
board = [[BLACK for _ in range(10)] for _ in range(20)]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Define functions
def draw_board():
    for y in range(20):
        for x in range(10):
            pygame.draw.rect(screen, board[y][x], pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_piece(piece, piece_x, piece_y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j]:
                pygame.draw.rect(screen, COLORS[piece_color_index], pygame.Rect((j + piece_x) * BLOCK_SIZE, (i + piece_y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def is_valid_position(piece, piece_x, piece_y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j]:
                x_pos = j + piece_x
                y_pos = i + piece_y
                if x_pos < 0 or x_pos >= 10 or y_pos >= 20 or board[y_pos][x_pos] != BLACK:
                    return False
    return True

def merge_piece(piece, piece_x, piece_y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j]:
                x_pos = j + piece_x
                y_pos = i + piece_y
                board[y_pos][x_pos] = COLORS[piece_color_index]
    check_full_lines()

def check_full_lines():
    global board, score
    new_board = [row for row in board if BLACK in row]
    lines_deleted = len(board) - len(new_board)
    score += lines_deleted * 5  # Update the score
    for _ in range(lines_deleted):
        new_board.insert(0, [BLACK for _ in range(10)])
    board = new_board

def check_game_over(piece_y):
    global running
    if piece_y <= 0:
        running = False

def move_piece(piece, piece_x, piece_y):
    if is_valid_position(piece, piece_x, piece_y + 1):
        return piece_x, piece_y + 1
    else:
        merge_piece(piece, piece_x, piece_y)
        return new_piece()

def rotate_piece(piece):
    return [list(row)[::-1] for row in zip(*piece)]

def new_piece():
    global piece_color_index
    piece_color_index = random.randint(0, len(COLORS) - 1)
    return random.choice(SHAPES), 3, 0

# Game initialization
score = 0
piece, piece_x, piece_y = new_piece()
last_move_time = pygame.time.get_ticks()
fall_speed = 500  # Milliseconds per step
fall_time = 0
running = True

# Main game loop
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and is_valid_position(piece, piece_x - 1, piece_y):
                piece_x -= 1
            elif event.key == pygame.K_RIGHT and is_valid_position(piece, piece_x + 1, piece_y):
                piece_x += 1
            elif event.key == pygame.K_DOWN:
                fall_speed = 100  # Increase falling speed
            elif event.key == pygame.K_SPACE:  # Rotate piece
                rotated_piece = rotate_piece(piece)
                if is_valid_position(rotated_piece, piece_x, piece_y):
                    piece = rotated_piece
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                fall_speed = 500  # Reset falling speed

    # Move piece down automatically
    now = pygame.time.get_ticks()
    fall_time += now - last_move_time
    last_move_time = now
    if fall_time > fall_speed:
        fall_time = 0
        if is_valid_position(piece, piece_x, piece_y + 1):
            piece_y += 1
        else:
            merge_piece(piece, piece_x, piece_y)
            piece, piece_x, piece_y = new_piece()

    # Draw the board and the piece
    draw_board()
    draw_piece(piece, piece_x, piece_y)

    # Draw the score
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Game over condition
    if not running:
        font = pygame.font.Font(None, 36)
        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        # Wait for a key press to close the game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    pygame.quit()
                    exit()

    pygame.display.flip()

pygame.quit()
