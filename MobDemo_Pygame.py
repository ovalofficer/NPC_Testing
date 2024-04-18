import pygame
import GameEntity
import random

# ======================================================= Simulation Settings

LOG_MOVES = False

BLOCK_SIZE = 10

# Sleep is in milliseconds
SLEEP = 25

DUDE_COUNT = 3

# ======================================================= PyGame Settings

pygame.init()

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720

WINDOW = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pygame.display.set_caption("NPC Demo")

AREA_X = WINDOW_WIDTH // BLOCK_SIZE
AREA_Y = WINDOW_HEIGHT // BLOCK_SIZE

FONT = pygame.font.SysFont("Consolas", BLOCK_SIZE, True)

COLORS = {
    "grid": (150, 150, 150),
    "background": (25, 25, 25),
    "trail": (255, 220, 220),
    "dude": (255, 0, 0),
    "goal": (255, 255, 0)
}


# ======================================================= Functions + Helpers

def get_random_map_point() -> tuple[int, int]:
    return random.randrange(0, AREA_X), random.randrange(0, AREA_Y)


def is_in_map_bounds(x, y) -> bool:
    return not (x <= 0 or x >= AREA_X or y <= 0 or y >= AREA_Y)


def draw_grid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            pygame.draw.rect(WINDOW, COLORS["grid"], (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)


def create_dudes(xy: tuple[int, int] = get_random_map_point(), xy_goal: tuple[int, int] = get_random_map_point()):
    dudes = []
    for i in range(1, DUDE_COUNT + 1):
        dudes.append(GameEntity.RadiantMob(f'Dude{i}', *xy, *xy_goal))
    return dudes


def check_starting_bounds(dudes: list[GameEntity.RadiantMob]):
    for dude in dudes:
        if not is_in_map_bounds(dude.x, dude.y):
            print(f'{dude.name} (INDEX {dude.index}) STARTING POS OUT OF BOUNDS')
            exit(1)


# ======================================================= Game Loop

running = True

dudes = create_dudes()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    WINDOW.fill(COLORS["background"])
    draw_grid()

    for dude in dudes:
        dude.desired_x, dude.desired_y = get_random_map_point()
        dude.update_path()

        for p in range(1, len(dude.path)):

            dude_label = FONT.render(f'{dude.index}', True, "white")
            next_x, next_y = dude.path[p]

            if LOG_MOVES:
                print(f'MOVE {p} : ({dude.name}): {dude.x}, {dude.y} -> {next_x, next_y}')

            dude.move(next_x, next_y)

            pygame.draw.rect(WINDOW, COLORS["goal"],
                             (dude.desired_x * BLOCK_SIZE, dude.desired_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            for v in range(1, p):
                pygame.draw.rect(WINDOW, COLORS["trail"],
                                 (dude.path[v][0] * BLOCK_SIZE, dude.path[v][1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            dude_rect = pygame.Rect(dude.x * BLOCK_SIZE, dude.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(WINDOW, COLORS["dude"],
                             dude_rect)

            dude_label_rect = pygame.Rect(dude.x * BLOCK_SIZE, dude.y * BLOCK_SIZE, BLOCK_SIZE // 2, BLOCK_SIZE // 2)
            WINDOW.blit(dude_label, dude_label_rect)

            pygame.display.flip()
            if SLEEP > 0:
                pygame.time.delay(SLEEP)

pygame.quit()
