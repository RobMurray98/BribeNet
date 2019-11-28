from abc import ABC


# abstract briber class
class Briber(ABC):
    def __init__(self, g, u0):
        self.u = u0  # resources of briber to spend
        self.g = g  # network for agent
        self.max_rating = self.g.max_rating
        self.spent = [0]

    def bribe(self, bribe_id, amount):
        if amount <= self.u:
            self.g.bribe(bribe_id, amount)
            self.u -= amount

    def next_bribe(self):
        pass

    def get_spent(self):
        return self.spent
