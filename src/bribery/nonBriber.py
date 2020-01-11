from bribery.briber import Briber


# performs no bribery
class NonBriber(Briber):

    def next_bribe(self):
        pass
