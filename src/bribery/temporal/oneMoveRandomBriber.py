import random

from bribery.briber import BriberyGraphNotSetException
from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction


class OneMoveRandomBriber(TemporalBriber):

    def next_action(self) -> SingleBriberyAction:
        if self._g is None:
            raise BriberyGraphNotSetException()
        customers = self._g.get_customers()
        # pick random customer from list
        c = random.choice(customers)
        max_rating = self._g.get_max_rating()
        if not self._g.get_vote(c):
            bribery_dict = {c: max_rating}
        else:
            bribery_dict = {c: max_rating - self._g.get_vote(c)[self.get_briber_id()]}
        return SingleBriberyAction(self, bribes=bribery_dict)
