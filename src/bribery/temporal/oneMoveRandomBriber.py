import random

from bribery.briber import BriberyGraphNotSetException
from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class OneMoveRandomBriber(TemporalBriber):

    def next_action(self) -> BriberyAction:
        if self._g is None:
            raise BriberyGraphNotSetException()
        customers = self._g.get_customers()
        # pick random customer from list
        c = random.choice(customers)
        max_rating = self._g.get_max_rating()
        if not self._g.get_vote(c):
            bribery_dict = {c: max_rating}
        else:
            bribery_dict = {c: max_rating - self._g.get_vote(c)}
        return BriberyAction(bribery_dict)
