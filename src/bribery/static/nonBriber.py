from bribery.static.briber import StaticBriber


# performs no bribery
class NonBriber(StaticBriber):

    def next_bribe(self):
        pass
