from Organisms.Organism import *
from constants import ORGANISM
from World.Position import Position
import random


class Animal(Organism):
    def action(self, key, mapping):
        directions = ["UP", "RIGHT", "LEFT", "DOWN"]
        random.shuffle(directions)
        while True:
            if len(directions) == 0:
                return False
            direction = directions.pop()
            if direction == "LEFT":
                if self.pos.x-1 >= 0:
                    # print("Poszedl w lewo")
                    self.pos.x -= 1
                    return True
            if direction == "RIGHT":
                if self.pos.x+1 < get_width():
                    # print("Poszedl w prawo")
                    self.pos.x += 1
                    return True
            if direction == "UP":
                if self.pos.y-1 >= 0:
                    # print("Poszedl w gore")
                    self.pos.y -= 1
                    return True
            if direction == "DOWN":
                if self.pos.y+1 < get_height():
                    # print("Poszedl w dol")
                    self.pos.y += 1
                    return True

    def collision(self, attacker, old_pos, *mapping):
        mapping = mapping[0]
        fight = True
        if self.name == attacker.name:
            fight = False
            mapping.cells[old_pos.y][old_pos.x].org = attacker
            if mapping.map_type == "AppHex":
                cells = Position.hex_get_adjacent(Position(attacker.pos.x, attacker.pos.y))
            if mapping.map_type == "AppStandard":
                cells = Position.get_adjacent(Position(attacker.pos.x, attacker.pos.y))
            cells = [i for i in cells if mapping.cells[i.y][i.x].org == "null"]  # filter adjacent cells
            if len(cells) > 0:
                return [[f"{attacker.name} Breed between",
                         f"{old_pos} and {self.pos},",
                         f"Baby: {cells[0]}"], cells[0], fight]
            else:
                return [[f"Attempt breeding {attacker.name} failed."], "", fight]
        if attacker.strength > self.strength:  # todo: general fight
            mapping.cells[self.pos.y][self.pos.x].clear()

            mapping.cells[self.pos.y][self.pos.x].org = attacker
            self.alive = False
        return [[f"Fight between: {attacker.name} => {self.name}",
                 f"{15*' '}{attacker.strength}{(len(attacker.name)-len(str(attacker.strength)))*' '} => {self.strength}"],
                "",
                fight]

        # return attacker.strength < self.strength
