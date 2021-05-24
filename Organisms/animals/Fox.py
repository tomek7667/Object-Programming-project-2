from Organisms.Animal import *


class Fox(Animal):
    def can_safely_move(self, pos):
        if self.mapping.cells[pos.y][pos.x].org != "null":
            if self.mapping.cells[pos.y][pos.x].org.strength > self.strength:
                return False
        return True

    def action(self, key, mapping):
        self.mapping = mapping
        directions = ["UP", "RIGHT", "LEFT", "DOWN"]
        random.shuffle(directions)
        while True:
            if len(directions) == 0:
                return False
            direction = directions.pop()
            if direction == "LEFT":
                if self.pos.x-1 >= 0 and self.can_safely_move(Position(self.pos.x-1, self.pos.y)):
                    self.pos.x -= 1
                    return True
            if direction == "RIGHT":
                if self.pos.x+1 < get_width() and self.can_safely_move(Position(self.pos.x+1, self.pos.y)):
                    self.pos.x += 1
                    return True
            if direction == "UP":
                if self.pos.y-1 >= 0 and self.can_safely_move(Position(self.pos.x, self.pos.y-1)):
                    self.pos.y -= 1
                    return True
            if direction == "DOWN":
                if self.pos.y+1 < get_height() and self.can_safely_move(Position(self.pos.x, self.pos.y+1)):
                    self.pos.y += 1
                    return True
