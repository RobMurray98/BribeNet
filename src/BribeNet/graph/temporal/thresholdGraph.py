import random
from typing import List

import numpy as np

from BribeNet.graph.ratingGraph import DEFAULT_GEN
from BribeNet.graph.temporal.action.actionType import ActionType
from BribeNet.graph.temporal.action.customerAction import CustomerAction
from BribeNet.graph.temporal.ratingGraph import TemporalRatingGraph, BriberKeywordArgumentOutOfBoundsException

DEFAULT_THRESHOLD = 0.5
MIN_THRESHOLD = 0.0
MAX_THRESHOLD = 1.0


class ThresholdGraph(TemporalRatingGraph):

    def __init__(self, bribers, generator=DEFAULT_GEN, **kwargs):
        """
        Threshold model for temporal rating graph
        :param bribers: the bribers active on the network
        :param generator: the generator to be used to generate the customer graph
        :param kwargs: additional parameters to the threshold temporal rating graph
        :keyword threshold: float - threshold for being considered
        :keyword remove_no_vote: bool - whether to allow non voted restaurants
        :keyword q: float - percentage of max rating given to non voted restaurants
        :keyword pay: float - the amount of utility gained by a restaurant when a customer visits
        :keyword apathy: float - the probability a customer does not visit any restaurant
        """
        super().__init__(bribers, generator=generator, **kwargs)
        if "threshold" in kwargs:
            threshold = kwargs["threshold"]
            if not MIN_THRESHOLD <= threshold <= MAX_THRESHOLD:
                raise BriberKeywordArgumentOutOfBoundsException(
                    f"threshold={threshold} out of bounds ({MIN_THRESHOLD}, {MAX_THRESHOLD})")
            self._threshold: float = threshold
        else:
            self._threshold: float = DEFAULT_THRESHOLD

    def _customer_action(self):

        # obtain customers ratings before any actions at this step, assumes all customers act simultaneously
        curr_ratings: List[List[float]] = [[self.get_rating(n, b.get_briber_id(), nan_default=0) for b in self._bribers]
                                           for n in self.get_customers()]
        voted: List[List[bool]] = [[len(self._neighbours(n, b.get_briber_id())) > 0 for b in self._bribers]
                                   for n in self.get_customers()]

        action = CustomerAction(self)
        for bribery_action in self._last_bribery_actions:
            action.set_bribed_from_bribery_action(bribery_action)

        # for each customer
        for n in self.get_graph().iterNodes():
            # get weightings for restaurants
            # 0 if below_threshold, q if no votes
            weights = np.zeros(len(self._bribers))

            for b in range(0, len(self._bribers)):
                # Check for no votes
                if not voted[n][b]:
                    weights[b] = self._q
                # P-rating below threshold
                elif curr_ratings[n][b] < self._threshold:
                    weights[b] = 0
                # Else probability proportional to P-rating
                else:
                    weights[b] = curr_ratings[n][b]

            # no restaurants above threshold so no action for this customer
            if np.count_nonzero(weights) == 0:
                continue

            # select at random
            selected = random.choices(range(0, len(self._bribers)), weights=weights)[0]

            if random.random() >= self._apathy:  # has no effect by default (DEFAULT_APATHY = 0.0)
                if action.get_action_type(n) == ActionType.NONE:  # if not already selected or bribed
                    action.set_select(n, selected)

        return action
