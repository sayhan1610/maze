import pygame
import random
import os

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

# Levels configuration
LEVEL_SETTINGS = {
    0: 40,  # Very easy
    1: 35,
    2: 30,
    3: 25,
    4: 20,  # Default
    5: 15,
    6: 10,
    7: 8,
    8: 6,
    9: 5    # Hardest
}

# Initial level
current_level = 4

# Directions (Right, Left, Up, Down)
DIRS = [(1, 0), (-1, 0), (0, -1), (0, 1)]
# Bit mask for each direction
RIGHT, LEFT, UP, DOWN = 1, 2, 4, 8

# Cell dimensions and maze setup
CELL_SIZE = LEVEL_SETTINGS[current_level]
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
EXIT_X, EXIT_Y = COLS - 1, ROWS - 1

# Maze grid
maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Path to the audio files
audio_path = os.path.join(os.path.dirname(__file__), 'audio')

# Load sound effects
key_sound = pygame.mixer.Sound(os.path.join(audio_path, 'key.mp3'))
start_sound = pygame.mixer.Sound(os.path.join(audio_path, 'start.mp3'))
win_sound = pygame.mixer.Sound(os.path.join(audio_path, 'win.mp3'))

def is_valid(nx, ny):
    return 0 <= nx < COLS and 0 <= ny < ROWS and not visited[ny][nx]

def generate_simpler_maze(x, y):
    stack = [(x, y)]
    visited[y][x] = True

    while stack:
        cx, cy = stack[-1]
        directions = DIRS[:]
        random.shuffle(directions)
        moved = False

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if is_valid(nx, ny):
                # Update maze structure to ensure easy paths
                if dx == 1:  # Moving right
                    maze[cy][cx] |= RIGHT
                    maze[ny][nx] |= LEFT
                elif dx == -1:  # Moving left
                    maze[cy][cx] |= LEFT
                    maze[ny][nx] |= RIGHT
                elif dy == 1:  # Moving down
                    maze[cy][cx] |= DOWN
                    maze[ny][nx] |= UP
                elif dy == -1:  # Moving up
                    maze[cy][cx] |= UP
                    maze[ny][nx] |= DOWN

                visited[ny][nx] = True
                stack.append((nx, ny))
                moved = True
                break

        if not moved:
            stack.pop()

def reset_game():
    global player_x, player_y, CELL_SIZE, COLS, ROWS, EXIT_X, EXIT_Y, maze, visited
    player_x, player_y = 0, 0
    # Update cell size and maze dimensions based on the current level
    CELL_SIZE = LEVEL_SETTINGS[current_level]
    COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
    EXIT_X, EXIT_Y = COLS - 1, ROWS - 1
    # Regenerate maze
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
    generate_simpler_maze(0, 0)

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
        "Press 'I' to hide this instruction.",
        "Press ESC to pause game.",
        "Click from 0-9 once the game starts to pick a difficulty level."
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

def draw_pause_screen():
    font = pygame.font.Font(None, 48)
    pause_text = font.render("Paused", True, BLACK)
    resume_text = font.render("Press ENTER to Resume", True, BLACK)
    quit_text = font.render("Press Q to Quit to Home", True, BLACK)
    WIN.fill(WHITE)
    WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2 - 40))
    WIN.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))
    WIN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.update()

def main():
    global player_x, player_y, current_level
    state = 'start'  # Game state: 'start', 'playing', 'instructions', 'win', 'paused'
    
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
                pygame.mixer.Sound.play(start_sound)
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
            if keys[pygame.K_ESCAPE]:  # Pause the game
                state = 'paused'

            if keys[pygame.K_r]:  # Restart the game
                pygame.mixer.Sound.play(key_sound)
                reset_game()
                start_time = pygame.time.get_ticks()

            if keys[pygame.K_0]:  # Set level to 0
                current_level = 0
                reset_game()
            if keys[pygame.K_1]:  # Set level to 1
                current_level = 1
                reset_game()
            if keys[pygame.K_2]:  # Set level to 2
                current_level = 2
                reset_game()
            if keys[pygame.K_3]:  # Set level to 3
                current_level = 3
                reset_game()
            if keys[pygame.K_4]:  # Set level to 4 (default)
                current_level = 4
                reset_game()
            if keys[pygame.K_5]:  # Set level to 5
                current_level = 5
                reset_game()
            if keys[pygame.K_6]:  # Set level to 6
                current_level = 6
                reset_game()
            if keys[pygame.K_7]:  # Set level to 7
                current_level = 7
                reset_game()
            if keys[pygame.K_8]:  # Set level to 8
                current_level = 8
                reset_game()
            if keys[pygame.K_9]:  # Set level to 9
                current_level = 9
                reset_game()

            moved = False
            if keys[pygame.K_RIGHT] and player_x < COLS - 1 and (maze[player_y][player_x] & RIGHT):
                if not moved:
                    pygame.mixer.Sound.play(key_sound)
                player_x += 1
                moved = True
            if keys[pygame.K_LEFT] and player_x > 0 and (maze[player_y][player_x] & LEFT):
                if not moved:
                    pygame.mixer.Sound.play(key_sound)
                player_x -= 1
                moved = True
            if keys[pygame.K_UP] and player_y > 0 and (maze[player_y][player_x] & UP):
                if not moved:
                    pygame.mixer.Sound.play(key_sound)
                player_y -= 1
                moved = True
            if keys[pygame.K_DOWN] and player_y < ROWS - 1 and (maze[player_y][player_x] & DOWN):
                if not moved:
                    pygame.mixer.Sound.play(key_sound)
                player_y += 1
                moved = True

            if player_x == EXIT_X and player_y == EXIT_Y:
                state = 'win'
                elapsed_time = pygame.time.get_ticks() - start_time
                pygame.mixer.Sound.play(win_sound)

            WIN.fill(WHITE)
            draw_maze()
            draw_player()
            draw_exit()
            draw_timer(start_time)
            pygame.display.update()

        elif state == 'paused':
            draw_pause_screen()
            if keys[pygame.K_RETURN]:  # Resume the game
                state = 'playing'
            if keys[pygame.K_q]:  # Quit to home screen
                state = 'start'

        elif state == 'win':
            draw_win_screen(elapsed_time)
            if keys[pygame.K_r]:  # Replay the game
                state = 'start'

    pygame.quit()

if __name__ == "__main__":
    main()
