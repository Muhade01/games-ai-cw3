import pygame
import sys
from astar import astar  # Import A* function

pygame.init()

# Window setup
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Pacman")

# Colors (more vibrant)
DARK_BLUE = (10, 20, 80)  # Walls
LIGHT_GRAY = (200, 200, 200)  # Background
GOLD = (255, 215, 0)  # Pacman
ORANGE = (255, 165, 0)  # Ghost
LIME_GREEN = (50, 255, 50)  # A* path
WHITE = (255, 255, 255)  # Pellets

# Player (Pacman)
player_pos = [1, 1]

# Ghost setup
ghosts = [{'pos': [3, 3], 'path': [], 'timer': 0}]

# Pellets setup
pellets = []
for y in range(ROWS):
    for x in range(COLS):
        if (x, y) != (1, 1) and (x, y) != (3, 3):  # Skip Pacman and ghost start
            pellets.append((x, y))

# Score
score = 0
font = pygame.font.SysFont(None, 36)

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
        pygame.draw.rect(screen, LIME_GREEN, (x*tile_size + tile_size//4, y*tile_size + tile_size//4, tile_size//2, tile_size//2))

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(LIGHT_GRAY)

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

    # Check for pellet collection
    player_tile = (player_pos[0], player_pos[1])
    if player_tile in pellets:
        pellets.remove(player_tile)
        score += 10

    # Update ghost paths and movement
    for ghost in ghosts:
        ghost['timer'] += 1
        if ghost['timer'] >= 5 or not ghost['path']:
            ghost['path'] = astar(game_map, (ghost['pos'][1], ghost['pos'][0]), (player_pos[1], player_pos[0]))
            ghost['timer'] = 0
        if ghost['path'] and len(ghost['path']) > 1:
            next_pos = ghost['path'][1]
            ghost['pos'] = [next_pos[1], next_pos[0]]
            ghost['path'].pop(0)

    # Draw map
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            color = DARK_BLUE if tile == 1 else LIGHT_GRAY
            pygame.draw.rect(screen, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw pellets
    for pellet in pellets:
        x, y = pellet
        pygame.draw.circle(screen, WHITE, (x*TILE_SIZE + TILE_SIZE//2, y*TILE_SIZE + TILE_SIZE//2), 3)

    # Draw ghost paths
    for ghost in ghosts:
        if ghost['path']:
            draw_path(screen, ghost['path'], TILE_SIZE)

    # Draw player
    pygame.draw.circle(screen, GOLD, (player_pos[0]*TILE_SIZE + TILE_SIZE//2, player_pos[1]*TILE_SIZE + TILE_SIZE//2), TILE_SIZE//2 - 2)

    # Draw ghosts
    for ghost in ghosts:
        pygame.draw.rect(screen, ORANGE, (ghost['pos'][0]*TILE_SIZE + 2, ghost['pos'][1]*TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4))

    # Draw score
    score_text = font.render(f"Score: {score}", True, DARK_BLUE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(10)