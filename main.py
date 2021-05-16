import sys
from constants import *
from World.App_hex import AppHex
from World.App_standard import AppStandard
from Technical.Initializer import which_mode


def main():
    pg.init()
    pg.display.set_mode(SCREEN_SIZE)
    FONT = pg.font.SysFont("Arial", 22)
    mode = which_mode()
    if mode is not None:
        klass = globals()[mode]
        run = klass(FONT, mode)
        run.open_menu()
        run.main_loop()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    main()
