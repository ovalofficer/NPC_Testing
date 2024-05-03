import pygame
import GameEntity
import random

# ======================================================= Controls

print("""
CONTROLS:
SPACE: Clear Screen
UP ARROW: Increase Block Size
DOWN ARROW: Decrease Block Size
LEFT ARROW: Increase sleep / Decrease simulation speed
RIGHT ARROW: Decrease sleep / Increase simulation speed
Z: Toggle Grid
X: Toggle Square Movement
""")

# ======================================================= Simulation Settings

LOG_MOVES = False

BLOCK_SIZE = 15

# Sleep is in milliseconds
SLEEP = 50

DUDE_COUNT = 5

SQUARE_PATH = False

# ======================================================= PyGame Settings

pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("NPC Demo")

AREA_X = WINDOW_WIDTH // BLOCK_SIZE
AREA_Y = WINDOW_HEIGHT // BLOCK_SIZE

FONT = pygame.font.SysFont("Consolas", BLOCK_SIZE, True)
MENU_FONT = pygame.font.SysFont("Tahoma", 15)

COLORS = {
    "grid": (150, 150, 150),
    "background": (100, 75, 40),
    "trail": (200, 165, 120),
    "dude": (0, 0, 0),
    "goal": (255, 255, 0)
}


# ======================================================= Functions + Helpers

def get_random_map_point() -> tuple[int, int]:
    return random.randrange(0, AREA_X), random.randrange(0, AREA_Y)


def is_in_map_bounds(x, y) -> bool:
    return not (x <= 0 or x >= AREA_X or y <= 0 or y >= AREA_Y)


def draw_grid():
    WINDOW.fill(COLORS["background"])
    if not GRID:
        return
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            pygame.draw.rect(WINDOW, COLORS["grid"], (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)


def create_dudes(xy: tuple[int, int] = get_random_map_point(), xy_goal: tuple[int, int] = get_random_map_point()):
    dudes = []
    for i in range(1, DUDE_COUNT + 1):
        dudes.append(GameEntity.RadiantMob(f'Dude{i}', *xy, *xy_goal))
    return dudes


def update_font():
    global FONT
    FONT = pygame.font.SysFont("Consolas", BLOCK_SIZE, True)


def update_area():
    global AREA_X, AREA_Y
    AREA_X = WINDOW_WIDTH // BLOCK_SIZE
    AREA_Y = WINDOW_HEIGHT // BLOCK_SIZE
    update_font()


def handle_events():
    global RUNNING, BLOCK_SIZE, SLEEP, GRID, SQUARE_PATH

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                RUNNING = False
                break
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        draw_grid()
                    case pygame.K_DOWN:
                        BLOCK_SIZE = max(BLOCK_SIZE - 1, 1)
                        update_area()
                        draw_grid()
                        print(f'BLOCK_SIZE: {BLOCK_SIZE} | AREA_X: {AREA_X} | AREA_Y: {AREA_Y}')
                    case pygame.K_UP:
                        BLOCK_SIZE += 1
                        update_area()
                        draw_grid()
                        print(f'BLOCK_SIZE: {BLOCK_SIZE} | AREA_X: {AREA_X} | AREA_Y: {AREA_Y}')
                    case pygame.K_LEFT:
                        SLEEP = min(SLEEP + 5, 1000)
                        print('SLEEP:', SLEEP)
                    case pygame.K_RIGHT:
                        SLEEP = max(SLEEP - 5, 0)
                        print('SLEEP:', SLEEP)
                    case pygame.K_z:
                        print('GRID:', GRID)
                        GRID = not GRID
                        draw_grid()
                    case pygame.K_x:
                        print('SQUARE_PATH:', SQUARE_PATH)
                        SQUARE_PATH = not SQUARE_PATH


# ======================================================= Game Loop

RUNNING = True
GRID = True

dudes = create_dudes()
draw_grid()

while RUNNING:

    for dude in dudes:
        dude.desired_x, dude.desired_y = get_random_map_point()
        if SQUARE_PATH:
            dude.update_path_square()
        else:
            dude.update_path()

        for p in range(1, len(dude.path)):

            handle_events()

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
            dude_label = FONT.render(f'{dude.index}', True, "white")
            WINDOW.blit(dude_label, dude_label_rect)

            settings_rect = pygame.Rect(0, WINDOW_HEIGHT - 20, WINDOW_WIDTH, 20)
            settings_label = MENU_FONT.render(
                f'| UP/DN BLOCK_SIZE:{BLOCK_SIZE} | LT/RT SLEEP:{SLEEP} | X SQUARE_PATH:{SQUARE_PATH} | Z GRID:{GRID} |',
                True, (255, 255, 255, 80), True)
            WINDOW.blit(settings_label, settings_rect)

            pygame.display.flip()

            if SLEEP > 0:
                pygame.time.delay(SLEEP)

pygame.quit()
