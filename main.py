import pygame
import sys
from astar import astar  # Import A* function

pygame.init()

# Window setup
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pacman")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player (Pacman)
player_pos = [1, 1]

# Ghost setup
ghosts = [{'pos': [3, 3], 'path': [], 'timer': 0}]  # One ghost at [3, 3]

# Simple map (1 = wall, 0 = empty)
game_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Function to draw A* path
def draw_path(screen, path, tile_size):
    for y, x in path:
        pygame.draw.rect(screen, GREEN, (x*tile_size + tile_size//4, y*tile_size + tile_size//4, tile_size//2, tile_size//2))

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 1 if game_map[player_pos[1]][player_pos[0]-1] == 0 else 0
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 1 if game_map[player_pos[1]][player_pos[0]+1] == 0 else 0
    if keys[pygame.K_UP]:
        player_pos[1] -= 1 if game_map[player_pos[1]-1][player_pos[0]] == 0 else 0
    if keys[pygame.K_DOWN]:
        player_pos[1] += 1 if game_map[player_pos[1]+1][player_pos[0]] == 0 else 0

    # Update ghost paths and movement
    for ghost in ghosts:
        ghost['timer'] += 1
        # Recalculate path every 5 frames (~0.5 seconds at 10 FPS)
        if ghost['timer'] >= 5 or not ghost['path']:
            ghost['path'] = astar(game_map, (ghost['pos'][1], ghost['pos'][0]), (player_pos[1], player_pos[0]))
            print("New path calculated:", ghost['path'])  # Debug
            ghost['timer'] = 0
        # Move ghost along path
        if ghost['path'] and len(ghost['path']) > 1:
            next_pos = ghost['path'][1]  # Next step
            ghost['pos'] = [next_pos[1], next_pos[0]]  # Update position
            ghost['path'].pop(0)  # Remove current step
            print("Ghost moving to:", ghost['pos'])  # Debug

    # Draw map
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            color = BLUE if tile == 1 else BLACK
            pygame.draw.rect(screen, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw ghost paths
    for ghost in ghosts:
        if ghost['path']:
            draw_path(screen, ghost['path'], TILE_SIZE)

    # Draw player
    pygame.draw.circle(screen, YELLOW, (player_pos[0]*TILE_SIZE + TILE_SIZE//2, player_pos[1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//2 - 2)

    # Draw ghosts
    for ghost in ghosts:
        pygame.draw.rect(screen, RED, (ghost['pos'][0]*TILE_SIZE + 2, ghost['pos'][1]*TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4))

    pygame.display.flip()
    clock.tick(10)