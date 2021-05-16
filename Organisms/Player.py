from Organisms.Animal import *
from constants import *


class Player(Animal):
    def action(self, key, mapping):
        if key == pg.K_LEFT:
            if self.pos.x-1 >= 0:
                self.pos.x -= 1
                return True
        if key == pg.K_RIGHT:
            if self.pos.x+1 < get_width():
                self.pos.x += 1
                return True
        if key == pg.K_DOWN:
            if self.pos.y+1 < get_height():
                self.pos.y += 1
                return True
        if key == pg.K_UP:
            if self.pos.y-1 >= 0:
                self.pos.y -= 1
                return True
        return False
