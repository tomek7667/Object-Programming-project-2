from Organisms.Plant import *


class Belladonna(Plant):
    def collision(self, attacker, old_pos, mapping):
        result = []
        self.alive = False
        result.append(self)
        result.append(attacker)
        msg = "Fight between: "
        result.append([
            f"{msg}{attacker.pos} {attacker.id}: {attacker.name} => {self.pos} {self.id}: {self.name}",
            f"{len(msg) * ' '}{attacker.strength}{(len(attacker.name) - len(str(attacker.strength))) * ' '} => {self.strength}"
        ])
        return result
