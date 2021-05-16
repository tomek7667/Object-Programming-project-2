import PySimpleGUI as sg
import random
import pygame as pg
import os
from World.size import *


class FileHandler:
    def __init__(self, debug=False):
        self.prefix = "[FileHandler]"
        self.debug = debug

    def save_file(self, tiles, seed):
        if self.debug:
            print(f"{self.prefix} {tiles}")
        event, values = sg.Window('Choose an option', [
            [sg.Text('Name of your save:')],
            [sg.InputText(key="filename")],
            [sg.Button('Ok'),
             sg.Button('Cancel')]
        ]).read(close=True)
        if event == "Ok":
            if len(values["filename"]) > 0:
                with open("states/"+values["filename"]+".save", "w") as f:
                    f.write(f"Seed: {seed}\n")
                    f.write(f"{get_width()} {get_height()}\n")
                    for tile in tiles:
                        if tile.org != "null":
                            f.write(f"{tile.org.name} {tile.org.pos.x} {tile.org.pos.y} {tile.org.strength} {tile.org.initiative} {tile.org.age} {tile.org.id}\n")

    def temp_file_init(self, values):
        if self.debug:
            print(f"{self.prefix} {values}")
        measurement = []
        if len(values["width"]) > 0 and int(values["width"]) > 0:
            measurement.append(int(values["width"]))
        else:
            measurement.append(10)
        if len(values["height"]) > 0 and int(values["height"]) > 0:
            measurement.append(int(values["height"]))
        else:
            measurement.append(10)
        if len(values["seed"]) > 0:
            measurement.append(int(values["seed"]))
        else:
            measurement.append(int(random.random()*(10**10)))
        with open("states/temp_file", 'w') as f:
            f.write(f"Seed: {measurement[2]}\n")
            f.write(f"{measurement[0]} {measurement[1]}\n")

    def temp_file_remove(self):
        if self.debug:
            print(f"{self.prefix} removing temp file")
        os.remove("states/temp_file")

    def get_states(self):
        if self.debug:
            print(f"{self.prefix} returning states")
        return os.listdir('states')
