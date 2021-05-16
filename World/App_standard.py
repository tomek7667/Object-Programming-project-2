from World.Reporter import Reporter
from World.StandardWorld.Tile import Tile
from World.StandardWorld.SCursorHighlight import *
from World.MapGen import MapGen
from World.Position import *
from Technical.FileHandler import FileHandler
from World.size import *
import PySimpleGUI as sg
from World.OrganismImports.OrganismImports import *


class AppStandard(object):
    def __init__(self, FONT, mode):
        self.mode = mode
        self.scale = 32
        self.capture_movement = False
        self.mapping = None
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.tiles = None  # self.make_map()
        self.font = FONT
        self.cursor = None
        self.reporter = Reporter(self.screen)
        self.file_handler = FileHandler()

    def make_map(self):
        tiles = pg.sprite.LayeredUpdates()
        start_x, start_y = self.screen_rect.midtop
        start_x -= 300
        start_y += self.scale + 16
        offset = self.scale
        for y in range(get_height()):
            for x in range(get_width()):
                org = self.mapping.cells[y][x]
                pos = (start_x + offset * x,
                       start_y + offset * y)
                Tile(pos, org, self.scale, tiles)
        return tiles

    def update(self):
        for sprite in self.tiles:
            if sprite.layer != sprite.rect.bottom:
                self.tiles.change_layer(sprite, sprite.rect.bottom)
        self.tiles.update()
        self.cursor.update(pg.mouse.get_pos(), self.tiles, self.screen_rect)

    def render(self):
        pg.display.set_mode(SCREEN_SIZE)  # resize
        self.screen = pg.display.get_surface()
        self.screen.fill(BACKGROUND)
        self.tiles.draw(self.screen)
        self.cursor.draw(self.screen)
        self.reporter.display_help()
        self.reporter.display_events()
        pg.display.update()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_LEFT, pg.K_UP, pg.K_DOWN, pg.K_RIGHT]:
                    self.reporter.clear()
                    self.next_turn(event.key)
                if event.key == pg.K_s:
                    self.file_handler.save_file(self.tiles, self.mapping.seed)
                if event.key == pg.K_l:
                    self.open_menu()
                if event.key == pg.K_c:
                    self.capture_movement = not self.capture_movement
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # left click
                    self.add_organism()
                if event.button == 4:
                    # scroll up
                    if self.scale > 10:
                        self.scale += 4
                    else:
                        self.scale += 1
                    self.cursor = SCursorHighlight(self.font, self.mapping, self.scale)
                    self.tiles = self.make_map()
                if event.button == 5:
                    # scroll down
                    if self.scale > 10:
                        self.scale -= 4
                    elif self.scale > 1:
                        self.scale -= 1
                    self.cursor = SCursorHighlight(self.font, self.mapping, self.scale)
                    self.tiles = self.make_map()

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def create_world(self):
        event, values = sg.Window('Choose an option', [
            [sg.Text('Specify the board height and width:')],
            [sg.Text('(default: 10)')],
            [sg.Text('Width:'), sg.InputText(size=(24, 1), key="width")],
            [sg.Text('Height:'), sg.InputText(size=(24, 1), key="height")],
            [sg.Text('Seed:'), sg.InputText(size=(24, 1), key="seed")],
            [sg.Button('Ok'),
             sg.Button('Cancel')]]
                                  ).read(close=True)
        if event == "Ok":
            self.file_handler.temp_file_init(values)
            self.mapping = MapGen("temp_file", self.mode)
            self.cursor = SCursorHighlight(self.font, self.mapping, self.scale)
            self.tiles = self.make_map()
            self.file_handler.temp_file_remove()
            self.reporter.clear()
        if event == "Cancel":
            self.open_menu()

    def open_menu(self):
        options = self.file_handler.get_states()
        if len(options) == 0:
            options.append("")
        event, values = sg.Window('Choose an option', [
            [sg.Text('Choose the save you want to load:')],
            [sg.Listbox(options,
                        size=(
                            len(max(options, key=len)) * 2,
                            len(options)),
                        key='chosen_save')],
            [sg.Button('Ok'),
             sg.Button('Cancel'),
             sg.Button('New World')]]
                                  ).read(close=True)
        if event == "Ok" and len(values["chosen_save"]) == 1 and len(values) != 0 and len(options) != 0 and options[0] != "":
            self.mapping = MapGen(values["chosen_save"][0], self.mode)
            self.cursor = SCursorHighlight(self.font, self.mapping, self.scale)
            self.tiles = self.make_map()
        elif event == "New World":
            self.create_world()
        elif event == "Cancel":
            if self.mapping is None:
                exit(1)
            pass
        elif event is None:
            if self.mapping is None:
                exit(1)
            pass
        else:
            sg.popup("You cannot do this. (Error: 203)")
            self.open_menu()

    def add_organism(self, given=False):
        if not given:
            pos = pg.mouse.get_pos()
        else:
            pos = given
        selected = [s for s in self.tiles if s.rect.collidepoint(pos)]
        player_on_map = 0
        for y in range(get_height()):
            for x in range(get_width()):
                if not self.mapping.cells[y][x].empty() and self.mapping.cells[y][x].org.name == "Player":
                    player_on_map = 1
        if len(selected) != 0 and selected[-1].org == "null":
            sc = selected[-1]  # selected_cell | shortened for other lines
            options = [i[0] for i in ORGANISM[player_on_map:] if i[0] != "null"]
            event, values = sg.Window('Choose an option', [
                [sg.Text('Which organism to be put')],
                [sg.Listbox(options,
                            size=(
                                len(max(options, key=len)) + 2,
                                len(options)),
                            key='chosen_organism')],
                [sg.Text("Properties (default if none provided):")],
                [[sg.Text('Strength', size=(9, 1)),
                  sg.InputText(key="strength", size=(5, 1))],
                 [sg.Text('Initiative', size=(9, 1)),
                  sg.InputText(key="initiative", size=(5, 1))],
                 [sg.Text('Age', size=(9, 1)),
                  sg.InputText(key="age", size=(5, 1))],
                 ],
                [sg.Button('Ok'),
                 sg.Button('Cancel')]]
                                      ).read(close=True)
            if event == 'Ok':
                if not len(values["chosen_organism"]) > 0 or not len(values["chosen_organism"][0]) > 0:
                    sg.popup("You need to select an organism.")
                    self.add_organism(pos)
                    return
                klass = globals()[values["chosen_organism"][0]]
                default_values = [org for org in ORGANISM if org[0] == values["chosen_organism"][0]][0]
                if len(values["strength"]) > 0:
                    temp_strength = int(values["strength"])
                else:
                    temp_strength = default_values[2]
                if len(values["initiative"]) > 0:
                    temp_initiative = int(values["initiative"])
                else:
                    temp_initiative = default_values[3]
                if len(values["age"]) > 0:
                    temp_age = int(values["age"])
                else:
                    temp_age = default_values[1]
                self.mapping.cells[sc.pos.y][sc.pos.x].org = klass(
                    values["chosen_organism"][0],
                    temp_strength,
                    temp_initiative,
                    Position(sc.pos.x, sc.pos.y),
                    temp_age,
                    self.mapping.new_id()
                )
                self.cursor = SCursorHighlight(self.font, self.mapping, self.scale)
                self.tiles = self.make_map()

    def next_turn(self, key):
        # player_cell = [self.tiles.get_sprite(i) for i in range(len(self.tiles)) if self.tiles.get_sprite(
        # i).org_name == "Player"][0]
        organism_cells = []
        for i in range(len(self.tiles)):
            if self.tiles.get_sprite(i).org_name != "null":
                organism_cells.append(self.tiles.get_sprite(i))
        organism_cells.sort(key=lambda t: (t.org.initiative, t.org.age), reverse=True)
        for i in organism_cells:
            if i.org.alive:
                old_position = Position(i.org.pos.x, i.org.pos.y)
                self.mapping.cells[i.org.pos.y][i.org.pos.x].clear()
                i.org.action(key, self.mapping)
                y = i.org.pos.y
                x = i.org.pos.x
                if not self.mapping.cells[y][x].empty():
                    cell = self.mapping.cells[y][x].org.collision(i.org, old_position, self.mapping)
                    if self.mapping.cells[y][x].org != "null" and not cell[2]:  # Breed
                        # i.org.pos = old_position
                        # self.mapping.cells[old_position.y][old_position.x].org = i.org
                        for announcement in cell[0]:
                            self.reporter.add_event(announcement)
                        if type(cell[1]) == Position:
                            cell = cell[1]
                            klass = globals()[i.org.name]
                            child = [o for o in ORGANISM if o[0] == i.org.name][0]
                            self.mapping.cells[cell.y][cell.x].org = klass(child[0],
                                                                           child[2],
                                                                           child[3],
                                                                           cell,
                                                                           child[1],
                                                                           self.mapping.new_id()
                                                                           )
                            self.cursor.mapping = self.mapping
                            self.cursor.update_label(cell)
                    else:  # Fight
                        for announcement in cell[0]:
                            self.reporter.add_event(announcement)
                        if self.capture_movement:
                            self.reporter.add_event(f"{i.org.name} from {old_position} to {Position(x, y)}")
                        # self.cursor.update_label(Position(x, y))
                        # self.cursor.update_label(old_position)
                else:
                    self.mapping.cells[y][x].org = i.org
                    self.cursor.mapping = self.mapping
                    self.cursor.update_label(Position(x, y))
                    self.cursor.update_label(old_position)
        self.tiles = self.make_map()