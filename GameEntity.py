import random


class Wall:

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class RadiantMob:
    index = 0

    '''
    
    My Radiant AI Cycle:
    Generate new list of objectives on regular basis to be done at specified times -- "Major Tasks"
    While RadiantMob is not doing or pursuing a Major Task, complete random objectives from list of smaller, shorter 
    tasks. -- "Minor Tasks"
    
    Our major task -- Go to a specified point on the map; desired_x, desired_y. Stay until no steps left.
    Our minor tasks -- Wander using random points

    https://en.wikipedia.org/wiki/Radiant_AI
    
    "The Radiant AI system deals with NPC interactions and behavior. It allows non-player characters to dynamically
    react to and interact with the world around them. General goals, such as "Eat in this location at 2pm" are given
    to NPCs, and NPCs are left to determine how to achieve them. The absence of individual scripting for each 
    character allows for the construction of a world on a much larger scale than other games had developed, and aids in
    the creation of what Todd Howard described as an "organic feel" for the game."
    
    '''

    def __init__(self, name: str = "UnnamedRadiant", x: int = 0, y: int = 0, desired_x: int = 0, desired_y: int = 0):
        self.name = name
        self.x = x
        self.y = y
        self.desired_x = desired_x
        self.desired_y = desired_y
        self.trail = [(x, y)]
        self.index = RadiantMob.index
        self.path = self.create_new_path(self.desired_x, self.desired_y)
        RadiantMob.index += 1

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.trail.append((x, y))

    def get_distance_to_point(self, x, y) -> float:
        return abs(((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5)

    def get_distance_to_mob(self, target) -> float:
        return self.get_distance_to_point(target.x, target.y)

    def get_closest_mob(self, others):
        # Can probably find a better way; chooses closest that isn't itself
        closest = (others[0] if others[0] != self else others[-1])

        for mob in others:
            if mob.index == self.index:
                pass
            elif self.get_distance_to_mob(mob) < self.get_distance_to_mob(closest):
                closest = mob

        return closest

    def is_at_point(self, x: int, y: int):
        return self.x == x and self.y == y

    # I dont know what to do with is_within yet -- could be static or

    def is_within(self, x: int, y: int, x1: int, y1: int, x2: int, y2: int):
        return x1 <= x <= x2 and y1 <= y <= y2

    def is_hitting_wall(self, wall: Wall):
        return self.is_within(self.x, self.y, wall.x1, wall.y1, wall.x2, wall.y2)

    # TODO:
    # Make method to circumvent wall; if x + 1 is wall, check x + 2, if out of bounds, check x - 1, etc.

    def create_new_path(self, dx: int, dy: int):
        sim_x, sim_y = self.x, self.y
        path = [(sim_x, sim_y)]

        while not sim_x == dx or not sim_y == dy:

            if sim_x < dx:
                sim_x += 1
            elif sim_x > dx:
                sim_x -= 1
            else:
                pass
            if sim_y < dy:
                sim_y += 1
            elif sim_y > dy:
                sim_y -= 1
            else:
                pass

            path.append((sim_x, sim_y))

        return path

    def create_new_path_random(self, dx: int, dy: int):
        sim_x, sim_y = self.x, self.y
        path = [(sim_x, sim_y)]

        while not sim_x == dx or not sim_y == dy:

            if sim_y < dy:
                sim_y += 1
            elif sim_y > dy:
                sim_y -= 1
            else:
                pass

            if sim_x < dx:
                sim_x += 1
            elif sim_x > dx:
                sim_x -= 1
            else:
                pass

            path.append((sim_x, sim_y))

        return path

    def update_path(self):
        self.path = self.create_new_path(self.desired_x, self.desired_y)

    def update_path_random(self):
        self.path = self.create_new_path_random(self.desired_x, self.desired_y)
