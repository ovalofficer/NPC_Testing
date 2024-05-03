import Entity
import random
import time

AREA_X = 50
AREA_Y = 30

GRID_EMPTY_SPACE = '.'
GRID_FILLED_SPACE = '_'

LOG_MOVES = True

# For radiance, this counts the number of objectives to randomly create
TASKS = 4

SLEEP = 0.25


def get_random_map_point() -> tuple[int, int]:
    return random.randrange(0, AREA_X + 1), random.randrange(0, AREA_Y + 1)


def is_in_map_bounds(x, y) -> bool:
    return not (x <= 0 or x >= AREA_X or y <= 0 or y >= AREA_Y)


def draw_grid(mobs: list[Entity.RadiantMob], walls: list[Entity.Wall]) -> None:
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
                if mob.trail[0][0] == x and mob.trail[0][1] == y:
                    print(f"\b{mob.index}", end='', sep='')
                if mob.x == x and mob.y == y:
                    print("\b" * len(str(mob.index) + ">x"), str(mob.index) + ">x", end='', sep='')
                if mob.desired_x == x and mob.desired_y == y:
                    print("\b" * len(str(mob.index) + ">o"), str(mob.index) + ">o", end='', sep='')

            for wall in walls:
                if wall.x1 <= x <= wall.x2 and wall.y1 <= y <= wall.y2:
                    print("\b#", end='')

        print(y + 1, end='')


def main():
    dude0 = Entity.RadiantMob("Dude0", 1, 1, *get_random_map_point())
    dude1 = Entity.RadiantMob("Dude1", *get_random_map_point(), *get_random_map_point())
    dudes = [dude0, dude1]

    wall1 = Entity.Wall(20, 5, 25, 8)

    walls = [wall1]

    for dude in dudes:

        if not is_in_map_bounds(dude.x, dude.y):
            print(f'{dude.name} (INDEX {dude.index}) STARTING POS OUT OF BOUNDS')
            exit(1)

        for i in range(TASKS):
            move = 0
            dude.desired_x, dude.desired_y = get_random_map_point()

            dude.update_path()
            while not dude.is_at_point(dude.desired_x, dude.desired_y):
                print(f'\n\t MOVE {move + 1}\n')

                next_x, next_y = dude.path[move]

                if LOG_MOVES:
                    print(f'{dude.name}: {dude.x}, {dude.y} -> {next_x, next_y}')

                dude.move(next_x, next_y)

                move += 1

                draw_grid(dudes, walls)
                if SLEEP > 0:
                    time.sleep(SLEEP)


main()
