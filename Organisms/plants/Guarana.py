from Organisms.Plant import *


class Guarana(Plant):
    def collision(self, attacker, old_pos, mapping):
        result = []
        self.alive = False
        attacker.strength += 3
        if attacker.strength >= self.strength:
            result.append(attacker)
            result.append(self)
        else:
            result.append(self)
            result.append(attacker)

        result.append([
            f"Fight between: {attacker.pos} {attacker.id}: {attacker.name} => {self.pos} {self.id}: {self.name}",
            f"{15 * ' '}{attacker.strength}{(len(attacker.name) - len(str(attacker.strength))) * ' '} => {self.strength}"
        ])
        return result
