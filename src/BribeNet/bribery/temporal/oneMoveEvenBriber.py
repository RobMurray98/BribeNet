import random

import numpy as np

from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.bribery.temporal.briber import TemporalBriber


class OneMoveEvenBriber(TemporalBriber):

    def _next_action(self) -> SingleBriberyAction:
        customers = self.get_graph().get_customers()
        # pick random customer from list
        c = random.choice(list(filter(lambda x: x % 2 == 0, customers)))
        max_rating = self.get_graph().get_max_rating()
        vote = self.get_graph().get_vote(c)[self.get_briber_id()]
        resources = self.get_resources()
        if np.isnan(vote):
            bribery_dict = {c: min(resources, max_rating)}
        else:
            bribery_dict = {c: min(resources, max_rating - vote)}
        return SingleBriberyAction(self, bribes=bribery_dict)
