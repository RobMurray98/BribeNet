from BribeNet.bribery.static.briber import StaticBriber


# performs no bribery
class NonBriber(StaticBriber):

    def _next_bribe(self):
        pass
