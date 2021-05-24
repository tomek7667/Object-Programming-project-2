from World.outline_render import *
from World.OrganismImports.OrganismImports import *

class MapGen(object):
    def __init__(self, file, map_type):
        self.map_type = map_type
        self.file = file
        self.seed = None
        self.ids_on_map = []
        self.cells = self.import_map()

    def __str__(self):
        result = f"MapGenObject, map type: {self.map_type}, Save: {self.file}\n"
        result += f"Seed: {self.seed}, Cells:\n"
        for row in self.cells:
            for column in row:
                result += str(column)
                result += " "
            result += "\n"
        return result

    def import_map(self):
        cells = []
        lines = []
        with open("states/" + str(self.file), "r") as f:
            for line in f:
                if line[0] != "#":
                    if line[-1] == '\n':
                        line = line[:-1]
                    lines.append(line)
        seed = lines.pop(0).split("Seed: ")[1]
        random.seed(int(seed))
        self.seed = seed
        organisms = [i.split(' ') for i in lines]
        with open("World/temp.conf", "w") as f:
            f.write(str(organisms[0]))
        organisms[0] = [int(i) for i in organisms[0]]
        WIDTH, HEIGHT = organisms.pop(0)
        for y in range(HEIGHT):
            temp = []
            for x in range(WIDTH):
                temp.append(Cell(Position(x, y)))
            cells.append(temp)
        for org in organisms:
            klass = globals()[org[0]]
            temp_name = org[0]
            temp_x = int(org[1])
            temp_y = int(org[2])
            temp_strength = int(org[3])
            temp_initiative = int(org[4])
            temp_age = int(org[5])
            temp_id = int(org[6])
            self.ids_on_map.append(temp_id)
            cells[temp_y][temp_x].org = klass(temp_name,
                                              temp_strength,
                                              temp_initiative,
                                              Position(temp_x, temp_y),
                                              temp_age,
                                              temp_id
                                              )
        return cells

    def new_id(self):
        if len(self.ids_on_map) > 0:
            self.ids_on_map.sort()
            self.ids_on_map.append(self.ids_on_map[-1]+1)
        else:
            self.ids_on_map = [1]
        return self.ids_on_map[-1]
