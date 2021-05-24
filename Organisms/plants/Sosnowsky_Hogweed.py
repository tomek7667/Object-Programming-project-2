from Organisms.Plant import *


class Sosnowsky_Hogweed(Plant):
    def action(self, key, mapping):
        self.mapping = mapping
        positions = []
        if mapping.map_type == "AppHex":
            if self.pos.x-1 >= 0:
                if self.pos.y-1 >= 0:
                    if self.mapping.cells[self.pos.y-1][self.pos.x-1].org != "null" and not issubclass(type(self.mapping.cells[self.pos.y-1][self.pos.x-1].org), Plant):
                        positions.append(Position(self.pos.x-1, self.pos.y-1))
            if self.pos.x+1 < get_width():
                if self.pos.y+1 < get_height():
                    if self.mapping.cells[self.pos.y+1][self.pos.x+1].org != "null" and not issubclass(type(self.mapping.cells[self.pos.y+1][self.pos.x+1].org), Plant):
                        positions.append(Position(self.pos.x+1, self.pos.y+1))
        if self.pos.x-1 >= 0:
            if self.mapping.cells[self.pos.y][self.pos.x-1].org != "null" and not issubclass(type(self.mapping.cells[self.pos.y][self.pos.x-1].org), Plant):
                positions.append(Position(self.pos.x-1, self.pos.y))
        if self.pos.x+1 < get_width():
            if self.mapping.cells[self.pos.y][self.pos.x+1].org != "null" and not issubclass(type(self.mapping.cells[self.pos.y][self.pos.x+1].org), Plant):
                positions.append(Position(self.pos.x+1, self.pos.y))
        if self.pos.y-1 >= 0:
            if self.mapping.cells[self.pos.y-1][self.pos.x].org != "null" and not issubclass(type(self.mapping.cells[self.pos.y-1][self.pos.x].org), Plant):
                positions.append(Position(self.pos.x, self.pos.y-1))
        if self.pos.y+1 < get_height():
            if self.mapping.cells[self.pos.y+1][self.pos.x].org != "null" and not issubclass(type(self.mapping.cells[self.pos.y+1][self.pos.x].org), Plant):
                positions.append(Position(self.pos.x, self.pos.y+1))
        if len(positions) != 0:
            return [positions, [f"{self.name} killed some animals around it!"]]
        return []