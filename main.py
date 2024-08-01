import pygame
import random


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

# Frame rate
FPS = 60

# Cell dimensions
CELL_SIZE = 20
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Directions (Right, Left, Up, Down)
DIRS = [(1, 0), (-1, 0), (0, -1), (0, 1)]

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
            maze[y][x] |= DIRS.index((dx, dy)) + 1
            maze[ny][nx] |= DIRS.index((-dx, -dy)) + 1
            generate_maze(nx, ny)

# Maze from top-left corner
generate_maze(0, 0)

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] & 1 == 0:  # Right wall
                pygame.draw.line(WIN, BLACK, (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 1)
            if maze[y][x] & 2 == 0:  # Left wall
                pygame.draw.line(WIN, BLACK, (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 1)
            if maze[y][x] & 4 == 0:  # Up wall
                pygame.draw.line(WIN, BLACK, (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE), 1)
            if maze[y][x] & 8 == 0:  # Down wall
                pygame.draw.line(WIN, BLACK, (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE), (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 1)

def draw_exit():
    pygame.draw.rect(WIN, GREEN, (EXIT_X * CELL_SIZE, EXIT_Y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Player starting position
player_x, player_y = 0, 0

def draw_player():
    pygame.draw.rect(WIN, RED, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_timer(start_time):
    font = pygame.font.Font(None, 36)
    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = elapsed_time // 60000
    seconds = (elapsed_time % 60000) // 1000
    timer_text = font.render(f"Time: {minutes}:{seconds:02d}", True, BLACK)
    WIN.blit(timer_text, (10, 10))

def main():
    global player_x, player_y

    clock = pygame.time.Clock()
    run = True
    start_time = pygame.time.get_ticks()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player_x < COLS - 1 and (maze[player_y][player_x] & 1):
            player_x += 1
        if keys[pygame.K_LEFT] and player_x > 0 and (maze[player_y][player_x] & 2):
            player_x -= 1
        if keys[pygame.K_UP] and player_y > 0 and (maze[player_y][player_x] & 4):
            player_y -= 1
        if keys[pygame.K_DOWN] and player_y < ROWS - 1 and (maze[player_y][player_x] & 8):
            player_y += 1

        if player_x == EXIT_X and player_y == EXIT_Y:
            print("You win!")
            run = False

        WIN.fill(WHITE)
        draw_maze()
        draw_player()
        draw_exit()
        draw_timer(start_time)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
