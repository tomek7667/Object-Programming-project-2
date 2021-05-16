from World.Position import *


class Cell:
    def __init__(self, pos, organism="null"):
        self.org = organism
        self.pos = pos

    def __str__(self):
        result = f"Cell at {self.pos}"
        if self.org != "null":
            result += f" containing: {self.org}"
        return result

    def clear(self):
        self.org = "null"

    def empty(self):
        return self.org == "null"
