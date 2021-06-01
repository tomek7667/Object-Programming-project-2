import pygame as pg
import PySimpleGUI as sg

sg.change_look_and_feel('DefaultNoMoreNagging')
appFont = ("Roboto", 18)
sg.set_options(font=appFont, button_color=('black', None))

TRANSPARENT = (0, 0, 0, 0)
SCREEN_SIZE = [1280, 720]
FPS = 60
BACKGROUND = pg.Color("darkslategray")

# age - strength - initiative
ORGANISM = [("Player", 0, 5, 4),
            ("Wolf", 0, 9, 5),
            ("Sheep", 0, 4, 4),
            ("Fox", 0, 3, 7),
            ("Turtle", 0, 2, 1),
            ("Antelope", 0, 4, 4),
            ("Cyber_sheep", 0, 11, 4),
            ("null", 0, 0, 0),
            ("Grass", 0, 0, 0),
            ("Sow_Thistle", 0, 0, 0),
            ("Guarana", 0, 0, 0),
            ("Belladonna", 0, 99, 0),
            ("Sosnowsky_Hogweed", 0, 10, 0)]

ORGANISM_COLORS = {"Player": pg.Color("cadetblue1"),
                   "Wolf": pg.Color("cornsilk4"),
                   "Fox": pg.Color("darkgoldenrod2"),
                   "Turtle": pg.Color("forestgreen"),
                   "Antelope": pg.Color("darksalmon"),
                   "Sheep": pg.Color("cornsilk1"),
                   "Cyber_sheep": pg.Color("gray13"),
                   "null": pg.Color("gray"),
                   "Grass": pg.Color("chartreuse3"),
                   "Sow_Thistle": pg.Color("chartreuse4"),
                   "Guarana": pg.Color("darkred"),
                   "Belladonna": pg.Color("darkorchid1"),
                   "Sosnowsky_Hogweed": pg.Color("burlywood4")
                   }

HELP = [
    "Tomasz Dabrowski s184571 - Politechnika Gdanska",
    "Press:",
    "[l] to load a map",
    "[s] to save a map",
    "[c] to turn movement capture",
    "[r] to activate purification",
    "Control with your arrow keys",
    "Move the map with [1, 2, 3, 4] or sroll"
]

MARGIN = 32
