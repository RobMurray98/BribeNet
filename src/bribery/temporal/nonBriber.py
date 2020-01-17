from bribery.temporal.briber import TemporalBriber


class TemporalNonBriber(TemporalBriber):

    def step(self):
        pass

    def next_bribe(self):
        pass
