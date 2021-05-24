from Organisms.Organism import *
from constants import ORGANISM
from World.Position import Position
import random


class Plant(Organism):
    def action(self, key, mapping):
        self.mapping = mapping
        positions = []
        if mapping.map_type == "AppHex":
            if self.pos.x-1 >= 0:
                if self.pos.y-1 >= 0:
                    if self.mapping.cells[self.pos.y-1][self.pos.x-1].org == "null":
                        positions.append(Position(self.pos.x-1, self.pos.y-1))
            if self.pos.x+1 < get_width():
                if self.pos.y+1 < get_height():
                    if self.mapping.cells[self.pos.y+1][self.pos.x+1].org == "null":
                        positions.append(Position(self.pos.x+1, self.pos.y+1))
        if self.pos.x-1 >= 0:
            if self.mapping.cells[self.pos.y][self.pos.x-1].org == "null":
                positions.append(Position(self.pos.x-1, self.pos.y))
        if self.pos.x+1 < get_width():
            if self.mapping.cells[self.pos.y][self.pos.x+1].org == "null":
                positions.append(Position(self.pos.x+1, self.pos.y))
        if self.pos.y-1 >= 0:
            if self.mapping.cells[self.pos.y-1][self.pos.x].org == "null":
                positions.append(Position(self.pos.x, self.pos.y-1))
        if self.pos.y+1 < get_height():
            if self.mapping.cells[self.pos.y+1][self.pos.x].org == "null":
                positions.append(Position(self.pos.x, self.pos.y+1))
        random.shuffle(positions)
        if len(positions) != 0 and random.randint(1, 4) == 1:
            return [[positions.pop()], [f"Spread succeeded - {self.name}"]]
        return []

    def collision(self, attacker, old_pos, mapping):
        result = []
        self.alive = False
        if attacker.strength >= self.strength:
            result.append(attacker)
            result.append(self)
        else:
            result.append(self)
            result.append(attacker)

        result.append([
            f"Fight between: {attacker.pos} {attacker.id}: {attacker.name} => {self.pos} {self.id}: {self.name}",
            f"{15 * ' '}{attacker.strength}{(len(attacker.name) - len(str(attacker.strength))) * ' '} => {self.strength}"
        ])
        return result
