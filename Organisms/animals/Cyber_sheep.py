from Organisms.Animal import *


class Cyber_sheep(Animal):
    def closest_hog_pos(self, h_poses):
        closest = {}
        for h_pos in h_poses:
            closest[h_pos] = abs(self.pos.x - h_pos.x) + abs(self.pos.y - h_pos.y)
        winner = list(closest.items())[0]
        for move in list(closest.items()):
            if winner[1] >= move[1]:
                winner = move
        return winner[0]

    def best_pos(self, h_pos, cells):
        best_move = {}
        for pos in cells:
            best_move[pos] = abs(pos.x - h_pos.x) + abs(pos.y - h_pos.y)
        winner = list(best_move.items())[0]
        for move in list(best_move.items()):
            if winner[1] >= move[1]:
                winner = move
        return winner

    def pos_of_hogweed(self):
        hogweeds = []
        for y in range(get_height()):
            for x in range(get_width()):
                if self.mapping.cells[y][x].org != "null" and self.mapping.cells[y][x].org.name == "Sosnowsky_Hogweed":
                    hogweeds.append(self.mapping.cells[y][x].pos)
        return hogweeds

    def action(self, key, mapping):
        self.mapping = mapping
        h_pos = self.pos_of_hogweed()
        if not h_pos:
            directions = ["UP", "RIGHT", "LEFT", "DOWN"]
            random.shuffle(directions)
            while True:
                if len(directions) == 0:
                    return False
                direction = directions.pop()
                if direction == "LEFT":
                    if self.pos.x-1 >= 0:
                        self.pos.x -= 1
                        return True
                if direction == "RIGHT":
                    if self.pos.x+1 < get_width():
                        self.pos.x += 1
                        return True
                if direction == "UP":
                    if self.pos.y-1 >= 0:
                        self.pos.y -= 1
                        return True
                if direction == "DOWN":
                    if self.pos.y+1 < get_height():
                        self.pos.y += 1
                        return True
        else:
            cells = []
            h_pos = self.closest_hog_pos(h_pos)
            if mapping.map_type == "AppHex":
                cells = Position.hex_get_adjacent(self.pos)
            if mapping.map_type == "AppStandard":
                cells = Position.get_adjacent(self.pos)
            self.pos = self.best_pos(h_pos, cells)[0]
            return True
