from Organisms.Plant import *


class Sow_Thistle(Plant):
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
        result = []
        for i in range(len(positions)):
            if i == 3:
                break
            if random.randint(1, 4) == 1:
                result.append(positions[i])
        if len(result) != 0:
            return [result, [f"Spread succeeded - {self.name}"]]
        return []
