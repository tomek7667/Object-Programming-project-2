from World.outline_render import *
from functools import cache


class Tile(pg.sprite.Sprite):  # todo 2
    def __init__(self, pos, cell, scale, *groups):
        self.scale = scale
        self.points = [0, 0], [0, scale*2], [scale*2, 0], [scale*2, 0]
        self.org = cell.org
        self.org_name = cell.org
        self.pos = cell.pos
        org_height = 0
        if cell.org != "null":
            self.org_name = cell.org.name
            org_height = cell.org.strength
        super(Tile, self).__init__(*groups)
        self.color = ORGANISM_COLORS[self.org_name]
        self.height = org_height
        self.image = self.make_tile()
        self.rect = self.image.get_rect(bottomleft=pos)
        self.mask = self.make_mask()

    def __str__(self):
        return f"StandardTile Object with org=[{self.org}] inside, at {self.pos}\n"

    def make_tile(self):
        points = self.points
        bottom = points
        image = pg.Surface((self.scale, self.scale))
        image.fill(TRANSPARENT)
        # bottom_col = [col for col in self.color[:3]]
        # pg.draw.polygon(image, bottom_col, bottom)
        pg.draw.polygon(image, self.color, points)
        pg.draw.lines(image, pg.Color("black"), True, points, 2)
        for start, end in zip(points[2:], bottom[2:]):
            pg.draw.line(image, pg.Color("black"), start, end, 1)
        pg.draw.lines(image, pg.Color("black"), 0, bottom[2:], 2)
        return image

    def make_mask(self):
        points = self.points
        temp_image = pg.Surface(self.image.get_size()).convert_alpha()
        temp_image.fill(TRANSPARENT)
        pg.draw.polygon(temp_image, pg.Color("red"), points)
        return pg.mask.from_surface(temp_image)
