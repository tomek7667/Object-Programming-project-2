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
            positions = [pos for pos in positions if self.mapping.cells[pos.y][pos.x].org != "null" and self.mapping.cells[pos.y][pos.x].org.name != "Cyber_sheep"]
            if len(positions) != 0:
                return [positions, [f"{self.name} killed some animals around it!"]]
            else:
                return []
        return []

    def collision(self, attacker, old_pos, mapping):
        result = []
        self.alive = False
        if attacker.name != "Cyber_sheep":
            result.append(self)
            result.append(attacker)
        else:
            result.append(attacker)
            result.append(self)
        msg = "Sosnowsky's hogweed has been eaten: "
        result.append([
            f"{msg}{attacker.pos} {attacker.id}: {attacker.name} => {self.pos} {self.id}: {self.name}",
            f"{len(msg) * ' '}{attacker.strength}{(len(attacker.name) - len(str(attacker.strength))) * ' '} => {self.strength}"
        ])
        return result
