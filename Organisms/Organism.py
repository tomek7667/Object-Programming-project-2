from constants import *
from World.size import *


class Organism:
    def __init__(self, name, strength, initiative, position, age, identificator):
        self.id = identificator
        self.took_under_account = False
        self.age = age
        self.name = name
        self.strength = strength
        self.initiative = initiative
        self.alive = True
        self.pos = position

    def __str__(self):
        return f"ID {self.id}, {self.name}, Age: {self.age} Strength: {self.strength}, Initiative: {self.initiative}, Alive: {self.alive}, Position: {self.pos}"

    def action(self, key, mapping):
        return [f'Base organism action {self}']

    def collision(self, attacker, old_pos, mapping):
        return [f"Base organism collision {self}"]
