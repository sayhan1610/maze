import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Automatic Maze Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Frame rate
FPS = 60

# Cell dimensions
CELL_SIZE = 20
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Directions (Right, Left, Up, Down)
DIRS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
# Bit mask for each direction
RIGHT, LEFT, UP, DOWN = 1, 2, 4, 8

# Maze grid
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Exit position
EXIT_X, EXIT_Y = COLS - 1, ROWS - 1

def is_valid(nx, ny):
    return 0 <= nx < COLS and 0 <= ny < ROWS and not visited[ny][nx]

def generate_maze(x, y):
    visited[y][x] = True
    directions = DIRS[:]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny):
            if dx == 1:  # Moving right
                maze[y][x] |= RIGHT
                maze[ny][nx] |= LEFT
            elif dx == -1:  # Moving left
                maze[y][x] |= LEFT
                maze[ny][nx] |= RIGHT
            elif dy == 1:  # Moving down
                maze[y][x] |= DOWN
                maze[ny][nx] |= UP
            elif dy == -1:  # Moving up
                maze[y][x] |= UP
                maze[ny][nx] |= DOWN
            generate_maze(nx, ny)

def reset_game():
    global player_x, player_y
    player_x, player_y = 0, 0
    # Regenerate maze
    global maze, visited
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    generate_maze(0, 0)

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] & RIGHT == 0:  # Right wall
                pygame.draw.line(WIN, BLACK, (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 1)
            if maze[y][x] & LEFT == 0:  # Left wall
                pygame.draw.line(WIN, BLACK, (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 1)
            if maze[y][x] & UP == 0:  # Up wall
                pygame.draw.line(WIN, BLACK, (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE), 1)
            if maze[y][x] & DOWN == 0:  # Down wall
                pygame.draw.line(WIN, BLACK, (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE), (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 1)

def draw_exit():
    pygame.draw.rect(WIN, GREEN, (EXIT_X * CELL_SIZE, EXIT_Y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player():
    pygame.draw.rect(WIN, RED, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_timer(start_time):
    font = pygame.font.Font(None, 36)
    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = elapsed_time // 60000
    seconds = (elapsed_time % 60000) // 1000
    timer_text = font.render(f"Time: {minutes}:{seconds:02d}", True, BLACK)
    WIN.blit(timer_text, (10, 10))

def draw_start_screen():
    font = pygame.font.Font(None, 48)
    text = font.render("Press ENTER to Start", True, BLACK)
    instructions = font.render("Press 'I' for Instructions", True, BLACK)
    WIN.fill(WHITE)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 20))
    WIN.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.update()

def draw_instructions_screen():
    font = pygame.font.Font(None, 36)
    lines = [
        "Use arrow keys to move.",
        "Reach the green square to win.",
        "Press 'R' to restart.",
        "Press 'I' to hide this instruction."
    ]
    WIN.fill(WHITE)
    y = 50
    for line in lines:
        text = font.render(line, True, BLACK)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 40
    pygame.display.update()

def draw_win_screen(elapsed_time):
    font = pygame.font.Font(None, 48)
    minutes = elapsed_time // 60000
    seconds = (elapsed_time % 60000) // 1000
    time_text = font.render(f"Time: {minutes}:{seconds:02d}", True, BLACK)
    replay_text = font.render("Press R to Replay", True, BLACK)
    WIN.fill(WHITE)
    WIN.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 - time_text.get_height() // 2 - 20))
    WIN.blit(replay_text, (WIDTH // 2 - replay_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.update()

def main():
    global player_x, player_y
    state = 'start'  # Game state: 'start', 'playing', 'instructions', 'win'
    
    clock = pygame.time.Clock()
    run = True
    start_time = None

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        
        if state == 'start':
            draw_start_screen()
            if keys[pygame.K_RETURN]:  # Start the game
                reset_game()
                start_time = pygame.time.get_ticks()
                state = 'playing'
            if keys[pygame.K_i]:  # Show instructions
                state = 'instructions'

        elif state == 'instructions':
            draw_instructions_screen()
            if keys[pygame.K_i]:  # Hide instructions
                state = 'start'

        elif state == 'playing':
            if keys[pygame.K_r]:  # Restart the game
                reset_game()
                start_time = pygame.time.get_ticks()

            if keys[pygame.K_RIGHT] and player_x < COLS - 1 and (maze[player_y][player_x] & RIGHT):
                player_x += 1
            if keys[pygame.K_LEFT] and player_x > 0 and (maze[player_y][player_x] & LEFT):
                player_x -= 1
            if keys[pygame.K_UP] and player_y > 0 and (maze[player_y][player_x] & UP):
                player_y -= 1
            if keys[pygame.K_DOWN] and player_y < ROWS - 1 and (maze[player_y][player_x] & DOWN):
                player_y += 1

            if player_x == EXIT_X and player_y == EXIT_Y:
                state = 'win'
                elapsed_time = pygame.time.get_ticks() - start_time

            WIN.fill(WHITE)
            draw_maze()
            draw_player()
            draw_exit()
            draw_timer(start_time)
            pygame.display.update()

        elif state == 'win':
            draw_win_screen(elapsed_time)
            if keys[pygame.K_r]:  # Replay the game
                state = 'start'

    pygame.quit()

if __name__ == "__main__":
    main()
