from typing import List

from graph.ratingGraph import DEFAULT_GEN
from graph.temporal.ratingGraph import TemporalRatingGraph

import numpy as np
import random

DEFAULT_THRESHOLD = 0.5
DEFAULT_REMOVE_NON_VOTED = False
DEFAULT_Q = 0.5
DEFAULT_PAY = 1.0
DEFAULT_APATHY = 0.0


class ThresholdGraph(TemporalRatingGraph):

    def __init__(self, bribers, generator=DEFAULT_GEN, **kwargs):
        """
        Threshold model for temporal rating graph
        :param bribers:
        :param generator:
        :param kwargs: additional parameters to the threshold temporal rating graph
        :keyword threshold: float - threshold for being considered
        :keyword remove_non_voted: bool - whether to allow non voted restaurants
        :keyword q: float - percentage of max rating given to non voted restaurants
        :keyword pay: float - the amount of utility gained by a restaurant when a customer visits
        :keyword apathy: float - the probability a customer does not visit any restaurant
        """
        super().__init__(bribers, generator=generator, **kwargs)
        if "threshold" in kwargs:
            self._threshold: float = kwargs["threshold"]
        else:
            self._threshold: float = DEFAULT_THRESHOLD
        if "remove_non_voted" in kwargs:
            self._remove_no_vote: bool = kwargs["remove_non_voted"]
        else:
            self._remove_no_vote: bool = DEFAULT_REMOVE_NON_VOTED
        if "q" in kwargs:
            self._q: float = kwargs["q"] * self._max_rating
        else:
            self._q: float = DEFAULT_Q * self._max_rating
        if "pay" in kwargs:
            self._pay: float = kwargs["pay"]
        else:
            self._pay: float = DEFAULT_PAY
        if "apathy" in kwargs:
            self._apathy: float = kwargs["apathy"]
        else:
            self._apathy: float = DEFAULT_APATHY

    def _customer_action(self):

        # obtain customers ratings before any actions at this step, assumes all customers act simultaneously
        curr_ratings: List[List[float]] = [[self.get_rating(n, b) for b in self._bribers] for n in self._g.nodes]
        voted: List[List[bool]] = [[len(self._neighbours(n, b)) > 0 for b in self._bribers] for n in self._g.nodes]

        # for each customer
        for n in self._g.nodes():
            # get weightings for restaurants
            # 0 if below_threshold, q if no votes
            weights = np.zeros(len(self._bribers))

            for b in range(0, len(self._bribers)):
                # Check for no votes
                if not voted[n][b]:
                    if self._remove_no_vote:
                        weights[b] = 0
                    else:
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
            selected = random.choices(range(0, len(self._bribers)), weights=weights)

            if random.random() >= self._apathy:  # has no effect by default (DEFAULT_APATHY = 0.0)
                # act on selection
                if self._votes[n][selected] == np.nan:  # no previous vote or bribe
                    self._votes[n][selected] = self._truths[n][selected]

                self._bribers[selected].add_resources(self._pay)
