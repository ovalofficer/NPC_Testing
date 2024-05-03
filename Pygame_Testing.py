import pygame
import GameEntity
import random
import time


WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720

BLOCK_SIZE = 20
GRID_MARGIN = 5

AREA_X = WINDOW_WIDTH // BLOCK_SIZE
AREA_Y = WINDOW_HEIGHT // BLOCK_SIZE

LOG_MOVES = True

TASKS = 1

# MILLISECONDS
SLEEP = 500

COLORS = {
    'empty': (150, 150, 150),
    'filled': (0, 150, 0),
    'wall': (150, 0, 0),
    'dude': (0, 0, 150),
    'dude_start': (150, 0, 150),
    'goal': (150, 150, 0)
}

# initializes pygame
pygame.init()

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Used so we can quit the process in the loop
running = True


def get_random_map_point() -> tuple[int, int]:
    return random.randrange(0, AREA_X + 1), random.randrange(0, AREA_Y + 1)


def is_in_map_bounds(x, y) -> bool:
    return not (x <= 0 or x >= AREA_X or y <= 0 or y >= AREA_Y)


def draw_grid() -> None:
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            pygame.draw.rect(WINDOW, (130, 130, 130), (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)


dude0 = GameEntity.RadiantMob("Dude0", 1, 1, *get_random_map_point())

dudes = [dude0]

while running:

    # pygame.QUIT is triggered when user clicks X button to close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    WINDOW.fill((100, 100, 100))

    draw_grid()

    for dude in dudes:
        pygame.draw.rect(WINDOW, COLORS['dude'], (dude.))

    # renders everything placed before this line
    pygame.display.update()

pygame.quit()
