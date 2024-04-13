import Entity
import random
import time

AREA_X = 90
AREA_Y = 30

MOVES = 50

# Maximum number of spaces to move per step
STEP_RANGE = 1

FORCE_INBOUNDS = True
FORCE_NO_BACKTRACK = True

MAX_BACKTRACK_ATTEMPTS = 5

GRID_EMPTY_SPACE = '.'
GRID_FILLED_SPACE = '_'

LOG_MOVES = True


def get_new_random_xy():
    return random.randrange(-STEP_RANGE, STEP_RANGE + 1), random.randrange(-STEP_RANGE, STEP_RANGE + 1)


def is_in_bounds(x, y):
    return not (x <= 0 or x >= AREA_X or y <= 0 or y >= AREA_Y)


def get_next_step(dude):
    rx, ry = get_new_random_xy()
    moves_tried = 0

    while not (FORCE_INBOUNDS and is_in_bounds(dude.x + rx, dude.y + ry)) or (
            FORCE_NO_BACKTRACK and (dude.x + rx, dude.y + ry) in dude.trail):
        rx, ry = get_new_random_xy()
        # print(f'{dude.name} tried to escape...')

        moves_tried += 1
        # print(f'{dude.name} tried backtracking {dude.x + rx, dude.y + ry}')

        if moves_tried > MAX_BACKTRACK_ATTEMPTS:
            print(f'({dude.name}) MAX BACKTRACKS REACHED - OVERRIDING')
            break

    return dude.x + rx, dude.y + ry


def draw_grid(mobs: list[Entity.Mob]) -> None:
    # print top coords
    # for i in range(1, AREA_X+1):
    #    print(i, end='')

    # Y
    for y in range(0, AREA_Y):
        print()
        # X
        for x in range(0, AREA_X):
            print(GRID_FILLED_SPACE, end='')

            for mob in mobs:
                for coords in mob.trail:
                    if coords[0] == x and coords[1] == y:
                        print(f'\b{GRID_EMPTY_SPACE}', end='')
                if mob.starting_x == x and mob.starting_y == y:
                    print(f"\b{mob.index}", end='', sep='')
                if mob.x == x and mob.y == y:
                    print("\b" * len(str(mob.index) + ">x"), str(mob.index) + ">x", end='', sep='')

        print(y + 1, end='')


def main():
    if STEP_RANGE > max(AREA_X, AREA_Y):
        print("STEP_RANGE LARGER THAN AREA")
        exit(1)

    dude0 = Entity.Mob("Dude0", 20, 15)
    dude1 = Entity.Mob("Dude1", 40, 15)
    dude2 = Entity.Mob("Dude2", 60, 25)

    dudes = [dude0, dude1, dude2]

    for dude in dudes:
        if not is_in_bounds(dude.x, dude.y):
            print(f'{dude.name} (INDEX {dude.index}) STARTING POS OUT OF BOUNDS')
            exit(1)

    for i in range(MOVES):
        print(f'\n\t MOVE {i + 1}\n')
        for dude in dudes:

            next_x, next_y = get_next_step(dude)

            if LOG_MOVES:
                print(f'{dude.name}: {dude.x}, {dude.y} -> {next_x, next_y}')

            dude.move(next_x, next_y)

            # print(f'{dude.trail}')

        draw_grid(dudes)
        time.sleep(0.35)


main()
