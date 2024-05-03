import random

class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(start):
    a_open = [start]
    a_closed = []

    while len(a_open) > 0:
        # q is least f node on list
        q = a_open[0]
        for n in a_open:
            if n.f < q:
                q = n
                a_open.remove(n)


class Wall:

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class AStarMob:
    index = 0

    def __init__(self, name: str = "UnnamedAstar", x: int = 0, y: int = 0, desired_x: int = 0, desired_y: int = 0):
        self.name = name
        self.x = x
        self.y = y
        self.desired_x = desired_x
        self.desired_y = desired_y
        self.trail = [(x, y)]
        self.index = AStarMob.index
        self.path = self.create_new_path(self.desired_x, self.desired_y)
        AStarMob.index += 1

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.trail.append((x, y))

    def get_distance_to_point(self, x, y) -> float:
        return abs(((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5)

    def is_at_point(self, x: int, y: int):
        return self.x == x and self.y == y

    def is_within(self, x1: int, y1: int, x2: int, y2: int):
        return x1 <= self.x <= x2 and y1 <= self.y <= y2

    def is_hitting_wall(self, wall: Wall):
        return self.is_within(wall.x1, wall.y1, wall.x2, wall.y2)

    def create_new_path(self, dx: int, dy: int):
        # F = G + H
        # F = total cost of the node
        # G - distance between current node and start node
        # H - heuristic - estimated distance from the current node to end node


    def update_path(self):
        self.path = self.create_new_path(self.desired_x, self.desired_y)
