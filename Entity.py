class Mob:
    index = 0

    def __init__(self, name: str = "Unnamed", x: int = 0, y: int = 0):
        self.name = name
        self.x = x
        self.y = y
        self.starting_x = x
        self.starting_y = y
        self.trail = [(x, y)]
        self.index = Mob.index
        Mob.index += 1

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.trail.append((x, y))

    def get_distance(self, target) -> float:
        return abs(((self.x - target.x) ** 2 + (self.y - target.y) ** 2) ** 0.5)

    def get_closest_mob(self, others):
        # Can probably find a better way; chooses closest that isn't itself
        closest = (others[0] if others[0] != self else others[-1])

        for mob in others:
            if mob.index == self.index:
                pass
            elif self.get_distance(mob) < self.get_distance(closest):
                closest = mob

        return closest

    