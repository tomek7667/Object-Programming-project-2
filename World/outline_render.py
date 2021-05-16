from World.Cell import *
from World.size import *

from constants import *


def outline_render(text, font, color, width, outline=pg.Color("black")):
    text_rend = font.render(text, 1, color)
    outline_rend = font.render(text, 1, outline)
    text_rect = text_rend.get_rect()
    final_rect = text_rect.inflate((width * 2, width * 2))
    text_rect.center = final_rect.center
    image = pg.Surface(final_rect.size).convert_alpha()
    image.fill(TRANSPARENT)

    for i in range(-width, width + 1):
        for j in range(-width, width + 1):
            pos_rect = text_rect.move(i, j)
            image.blit(outline_rend, pos_rect)
    image.blit(text_rend, text_rect)
    return image
