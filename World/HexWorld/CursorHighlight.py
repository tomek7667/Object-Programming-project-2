from World.outline_render import *


class CursorHighlight(pg.sprite.Sprite):
    FOOTPRINT_SIZE = (65, 32)
    COLOR = (50, 50, 200, 150)

    def __init__(self, FONT, mapping, *groups):
        super(CursorHighlight, self).__init__(*groups)
        self.font = FONT
        points = (8, 4), (45, 0), (64, 10), (57, 27), (20, 31), (0, 22)
        self.image = pg.Surface(self.FOOTPRINT_SIZE).convert_alpha()
        self.image.fill(TRANSPARENT)
        pg.draw.polygon(self.image, self.COLOR, points)
        self.rect = pg.Rect((0, 0, 1, 1))
        self.mask = pg.Mask((1, 1))
        self.mask.fill()
        self.target = None
        self.org = None
        self.org_name = None
        self.mapping = mapping
        self.label_dict = self.make_labels()
        self.label_image = None
        self.label_rect = None
    
    def update_label(self, pos):
        content = ""
        if not self.mapping.cells[pos.y][pos.x].empty():
            content = self.mapping.cells[pos.y][pos.x].org.name
            content += f" | ID: {self.mapping.cells[pos.y][pos.x].org.id}"
            content += f" | I: {self.mapping.cells[pos.y][pos.x].org.initiative}"
            content += f" | A: {self.mapping.cells[pos.y][pos.x].org.age} | "
        name = f"{pos.x} {pos.y}"
        content += f"x={pos.x} y={pos.y}"
        self.label_dict[name] = outline_render(content, self.font, pg.Color("white"), 3)

    def make_labels(self):
        labels = {}
        for y in range(get_height()):
            for x in range(get_width()):
                content = ""
                if not self.mapping.cells[y][x].empty():
                    content = self.mapping.cells[y][x].org.name
                    content += f" | ID: {self.mapping.cells[y][x].org.id}"
                    content += f" | I: {self.mapping.cells[y][x].org.initiative}"
                    content += f" | A: {self.mapping.cells[y][x].org.age} | "
                name = f"{x} {y}"
                content += f"x={x} y={y}"
                labels[name] = outline_render(content, self.font, pg.Color("white"), 3)
        return labels

    def update(self, pos, tiles, screen_rect):
        self.rect.topleft = pos
        hits = pg.sprite.spritecollide(self, tiles, 0, pg.sprite.collide_mask)
        if hits:
            true_hit = max(hits, key=lambda x: x.rect.bottom)
            self.target = true_hit.rect.topleft
            self.org_name = true_hit.org_name
            self.org = true_hit.org
            self.label_image = self.label_dict[f"{true_hit.pos.x} {true_hit.pos.y}"]
            self.label_rect = self.label_image.get_rect(midbottom=pos)
            self.label_rect.clamp_ip(screen_rect)
        else:
            self.org_name = None
            self.org = None

    def draw(self, surface):
        if self.org:
            surface.blit(self.image, self.target)
            surface.blit(self.label_image, self.label_rect)

