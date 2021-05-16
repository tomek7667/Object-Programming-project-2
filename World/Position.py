from World.size import *
import random


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x={self.x}, y={self.y}"

    def __len__(self):
        return 2

    def hex_get_adjacent(self):
        positions = []
        if self.x - 1 >= 0:
            positions.append(Position(self.x - 1, self.y))
            if self.y - 1 >= 0:
                positions.append(Position(self.x - 1, self.y - 1))
        if self.x + 1 < get_width():
            positions.append(Position(self.x + 1, self.y))
            if self.y + 1 < get_height():
                positions.append(Position(self.x + 1, self.y + 1))
        if self.y + 1 < get_height():
            positions.append(Position(self.x, self.y + 1))
        if self.y - 1 >= 0:
            positions.append(Position(self.x, self.y - 1))
        random.shuffle(positions)
        return positions

    def get_adjacent(self):
        positions = []
        if self.x - 1 >= 0:
            positions.append(Position(self.x - 1, self.y))
        if self.x + 1 < get_width():
            positions.append(Position(self.x + 1, self.y))
        if self.y + 1 < get_height():
            positions.append(Position(self.x, self.y + 1))
        if self.y - 1 >= 0:
            positions.append(Position(self.x, self.y - 1))
        random.shuffle(positions)
        return positions

