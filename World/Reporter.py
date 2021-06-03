from constants import *


class Reporter:
    def __init__(self, screen, map_type):
        self.screen = screen
        self.prefix = "[REPORTER]"
        self.events = []
        self.map_type = map_type
        self.font = pg.font.SysFont("consolas", 14)

    def display_help(self):
        if self.map_type == "Standard":
            HELP[-1] = "Use your scroll to resize the map"
        for i in range(len(HELP)):
            information = self.font.render(HELP[i], True, pg.Color("white"))
            self.screen.blit(information, (14, 14 * i + 14))

    def add_event(self, event):
        self.events.append(event)

    def display_events(self):
        if len(self.events) > 0:
            info = self.font.render(self.prefix, True, pg.Color("white"))
            self.screen.blit(info, (SCREEN_SIZE[0]-(len(max(self.events, key=len)))*9, 14))
            for i in range(len(self.events)):
                info = self.font.render(self.events[i], True, pg.Color("white"))
                self.screen.blit(info, (SCREEN_SIZE[0]-(len(max(self.events, key=len)))*9, 14 * (i+1) + 14))

    def clear(self):
        self.events = []
