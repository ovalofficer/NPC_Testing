import Entity


def main():
    dude0 = Entity.Mob("Dude0", 10, 10)
    dude1 = Entity.Mob("Dude1", 15, 15)
    dude2 = Entity.Mob("Dude2", 16, 16)
    dude3 = Entity.Mob("Dude3", 22, 31)
    dude4 = Entity.Mob("Dude4", 9, 5)

    dudes = [dude0, dude1, dude2, dude3, dude4]

    for dude in dudes:
        print(
            f'Dude {dude.index} ({dude.x}, {dude.y}) is closest to {dude.get_closest_mob(dudes).name} ({dude.get_distance(dude.get_closest_mob(dudes))})')

    dude2.move(25, 25)

    print()

    for dude in dudes:
        print(
            f'Dude {dude.index} ({dude.x}, {dude.y}) is closest to {dude.get_closest_mob(dudes).name} ({dude.get_distance(dude.get_closest_mob(dudes))})')


main()
