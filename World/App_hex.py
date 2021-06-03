from World.HexWorld.CursorHighlight import *
from World.HexWorld.HexTile import HexTile
from World.MapGen import MapGen
from World.Reporter import Reporter
from Technical.FileHandler import FileHandler
from World.OrganismImports.OrganismImports import *


class AppHex(object):
    def __init__(self, FONT, mode):
        self.mode = mode
        self.capture_movement = False
        self.mapping = None
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.tiles = None
        self.font = FONT
        self.cursor = None
        self.reporter = Reporter(self.screen)
        self.file_handler = FileHandler()
        self.organisms = {}
        self.cooldown = 0
        self.ability_on = False
        self.zoom = Position(100, 300)

    def make_map(self):
        tiles = pg.sprite.LayeredUpdates()
        start_x, start_y = self.screen_rect.midtop
        start_x -= self.zoom.x
        start_y += self.zoom.y
        row_offset = -45, 22
        col_offset = 57, 5
        for y in range(get_height()):
            for x in range(get_width()):
                org = self.mapping.cells[y][x]
                pos = (start_x + row_offset[0] * y + col_offset[0] * x,
                       start_y + row_offset[1] * y + col_offset[1] * x)
                HexTile(pos, org, tiles)
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
            self.cooldown = self.mapping.cooldown
            self.ability_on = self.mapping.active
            self.cursor = CursorHighlight(self.font, self.mapping)
            self.tiles = self.make_map()
            self.file_handler.temp_file_remove()
            self.reporter.clear()
        if event == "Cancel":
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
                self.cursor = CursorHighlight(self.font, self.mapping)
                self.tiles = self.make_map()

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
            self.cooldown = self.mapping.cooldown
            self.ability_on = self.mapping.active
            self.cursor = CursorHighlight(self.font, self.mapping)
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

    def activate_purification(self):
        self.reporter.clear()
        if not self.ability_on and self.cooldown <= 0:
            self.cooldown = 5
            self.ability_on = True
            self.reporter.add_event("Purification will be activated in the next round!")
            self.reporter.display_events()
        else:
            self.reporter.add_event("Purification is not done yet!")
            self.reporter.display_events()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_LEFT, pg.K_UP, pg.K_DOWN, pg.K_RIGHT]:
                    self.reporter.clear()
                    self.next_turn(event.key)
                if event.key == pg.K_s:
                    self.file_handler.save_file(self.tiles, self.mapping.seed, self.cooldown, self.ability_on)
                if event.key == pg.K_l:
                    self.open_menu()
                if event.key == pg.K_c:
                    self.capture_movement = not self.capture_movement
                if event.key == pg.K_r:
                    self.activate_purification()
                if event.key == pg.K_1:
                    self.zoom.y -= 50
                    self.tiles = self.make_map()
                if event.key == pg.K_2:
                    self.zoom.x -= 50
                    self.tiles = self.make_map()
                if event.key == pg.K_3:
                    self.zoom.y += 50
                    self.tiles = self.make_map()
                if event.key == pg.K_4:
                    self.zoom.x += 50
                    self.tiles = self.make_map()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # left click
                    self.add_organism()


    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def organism_get_key(self, org, orgs):
        for i in range(len(orgs)):
            if org.id == orgs[i].org.id:
                return i
        print("This should never happen!")

    def check_player(self, tried=0):
        player = []
        for asd in self.mapping.cells:
            player.append([True for jd in asd if jd.org != "null" and jd.org.name == "Player"])
        if [True] in player:
            print(f"\t\tjest gracz {tried}")
        else:
            print(f"\t\tni ma gracza {tried}")

    def next_turn(self, key):
        organism_cells = []
        self.ability_on = self.cooldown >= 0
        for i in range(len(self.tiles)):
            if self.tiles.get_sprite(i).org_name != "null" and self.tiles.get_sprite(i).org.alive:
                organism_cells.append(self.tiles.get_sprite(i))
        organism_cells.sort(key=lambda t: (t.org.initiative, t.org.age), reverse=True)
        for i in organism_cells:
            if i.org != "null" and i.org.alive:
                i.org.age += 1
                old_position = Position(i.org.pos.x, i.org.pos.y)
                self.mapping.cells[i.org.pos.y][i.org.pos.x].clear()
                moved = i.org.action([key, self.ability_on], self.mapping)
                if type(i.org) == Player and self.ability_on and moved and len(moved) != 0:
                    for announcement in moved[-1]:
                        self.reporter.add_event(announcement)
                    for p in moved[0]:
                        temp_org = self.mapping.cells[p.y][p.x].org
                        try:
                            organism_cells[self.organism_get_key(temp_org, organism_cells)].org.alive = False
                            organism_cells[self.organism_get_key(temp_org, organism_cells)].org = "null"
                        except:
                            pass
                            # self.check_player("Sosnowsky hex check3")
                        self.mapping.cells[p.y][p.x].org.alive = False
                        self.mapping.cells[p.y][p.x].org = "null"
                        self.mapping.cells[i.org.pos.y][i.org.pos.x].org = i.org
                        self.cursor.mapping = self.mapping
                        self.cursor.update_label(Position(i.org.pos.x, i.org.pos.y))
                elif issubclass(type(i.org), Animal):
                    if moved:
                        y = i.org.pos.y
                        x = i.org.pos.x
                        if self.capture_movement:
                            self.reporter.add_event(f"{i.org.id}: {i.org.name} from {old_position} to {Position(x, y)}")
                        if not self.mapping.cells[y][x].empty():
                            cell = self.mapping.cells[y][x].org.collision(i.org, old_position, self.mapping)
                            if (type(cell[0]) == Position or len(cell) == 1) and i.org.name != "Player":  # Breed
                                for announcement in cell[-1]:
                                    self.reporter.add_event(announcement)
                                if type(cell[0]) == Position:
                                    cell = cell[0]
                                    klass = globals()[i.org.name]
                                    child = [o for o in ORGANISM if o[0] == i.org.name][0]
                                    self.mapping.cells[cell.y][cell.x].org = klass(child[0],
                                                                                   child[2],
                                                                                   child[3],
                                                                                   cell,
                                                                                   child[1],
                                                                                   self.mapping.new_id()
                                                                                   )
                                i.org.pos = old_position
                                self.mapping.cells[old_position.y][old_position.x].org = i.org
                                self.cursor.mapping = self.mapping
                                self.cursor.update_label(Position(x, y))
                                self.cursor.update_label(old_position)
                            else:  # Fight
                                for announcement in cell[-1]:
                                    self.reporter.add_event(announcement)
                                rem = cell[0]
                                if rem == "turtle reflection":
                                    i.org.pos = old_position
                                    self.mapping.cells[old_position.y][old_position.x].org = i.org
                                elif rem == "Antelope runaway success":
                                    self.mapping.cells[cell[1].y][cell[1].x].org = self.mapping.cells[i.org.pos.y][i.org.pos.x].org
                                    self.mapping.cells[i.org.pos.y][i.org.pos.x].org = i.org
                                    self.cursor.update_label(cell[1])
                                    pass
                                else:
                                    if not isinstance(rem, type(self.mapping.cells[rem.pos.y][rem.pos.x].org)):
                                        self.mapping.cells[rem.pos.y][rem.pos.x].org.alive = False
                                        self.mapping.cells[rem.pos.y][rem.pos.x].org = "null"
                                        try:
                                            organism_cells[self.organism_get_key(cell[1], organism_cells)].org.alive = False
                                            organism_cells[self.organism_get_key(cell[1], organism_cells)].org = "null"
                                        except:
                                            pass
                                            # self.check_player("check 1")
                                    if issubclass(type(rem), Plant):  # case for plants
                                        self.mapping.cells[rem.pos.y][rem.pos.x].org = "null"
                                        try:
                                            organism_cells[self.organism_get_key(rem, organism_cells)].org.alive = False
                                            organism_cells[self.organism_get_key(rem, organism_cells)].org = "null"
                                        except:
                                            pass
                                            # self.check_player("check 2")
                                    else:
                                        self.mapping.cells[rem.pos.y][rem.pos.x].org = rem
                        else:
                            self.mapping.cells[y][x].org = i.org
                        self.cursor.mapping = self.mapping
                        self.cursor.update_label(Position(x, y))
                        self.cursor.update_label(old_position)
                    else:
                        self.mapping.cells[i.org.pos.y][i.org.pos.x].org = i.org
                        self.cursor.mapping = self.mapping
                        self.cursor.update_label(i.org.pos)
                        self.cursor.update_label(old_position)
                elif issubclass(type(i.org), Plant):
                    if type(i.org) == Sosnowsky_Hogweed:
                        if len(moved) != 0:
                            for announcement in moved[-1]:
                                self.reporter.add_event(announcement)
                            for p in moved[0]:
                                temp_org = self.mapping.cells[p.y][p.x].org
                                if temp_org.name != "Cyber_sheep":
                                    try:
                                        organism_cells[self.organism_get_key(temp_org, organism_cells)].org.alive = False
                                        organism_cells[self.organism_get_key(temp_org, organism_cells)].org = "null"
                                    except:
                                        pass
                                        # self.check_player("Sosnowsky hex check3")
                                    self.mapping.cells[p.y][p.x].org.alive = False
                                    self.mapping.cells[p.y][p.x].org = "null"
                            for c in moved[0]:
                                self.cursor.update_label(c)
                    elif len(moved) != 0:
                        for announcement in moved[-1]:
                            self.reporter.add_event(announcement)
                        for c in moved[0]:
                            klass = globals()[i.org.name]
                            child = [o for o in ORGANISM if o[0] == i.org.name][0]
                            self.mapping.cells[c.y][c.x].org = klass(child[0],
                                                                     child[2],
                                                                     child[3],
                                                                     c,
                                                                     child[1],
                                                                     self.mapping.new_id()
                                                                     )
                        self.cursor.mapping = self.mapping
                        for c in moved[0]:
                            self.cursor.update_label(c)
                    self.mapping.cells[i.org.pos.y][i.org.pos.x].org = i.org
                    self.cursor.mapping = self.mapping
                    self.cursor.update_label(Position(i.org.pos.x, i.org.pos.y))
        self.tiles = self.make_map()
        self.cooldown -= 1
