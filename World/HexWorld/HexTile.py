from World.outline_render import *
from functools import cache


class HexTile(pg.sprite.Sprite):
    def __init__(self, pos, cell, *groups):
        self.org = cell.org
        self.org_name = cell.org
        self.pos = cell.pos
        org_height = 0
        if cell.org != "null":
            self.org_name = cell.org.name
            org_height = cell.org.strength
        super(HexTile, self).__init__(*groups)
        self.color = ORGANISM_COLORS[self.org_name]
        self.height = org_height
        self.image = self.make_tile()
        self.rect = self.image.get_rect(bottomleft=pos)
        self.mask = self.make_mask()
        # self.layer = 0

    def __str__(self):
        return f"HexTile Object with org=[{self.org}] inside, at {self.pos}"

    def make_tile(self):
        h = self.height
        points = [8, 4], [45, 0], [64, 10], [57, 27], [20, 31], [0, 22]
        bottom = [points[-1], points[2]] + [(x, (y + h - 1)) for x, y in points[2:]]
        image = pg.Surface((65, 32 + h)).convert_alpha()
        image.fill(TRANSPARENT)
        bottom_col = [.5 * col for col in self.color[:3]]
        pg.draw.polygon(image, bottom_col, bottom)
        pg.draw.polygon(image, self.color, points)
        pg.draw.lines(image, pg.Color("black"), 1, points, 2)
        for start, end in zip(points[2:], bottom[2:]):
            pg.draw.line(image, pg.Color("black"), start, end, 1)
        pg.draw.lines(image, pg.Color("black"), 0, bottom[2:], 2)
        return image

    def make_mask(self):
        points = (8, 4), (45, 0), (64, 10), (57, 27), (20, 31), (0, 22)
        temp_image = pg.Surface(self.image.get_size()).convert_alpha()
        temp_image.fill(TRANSPARENT)
        pg.draw.polygon(temp_image, pg.Color("red"), points)
        return pg.mask.from_surface(temp_image)
