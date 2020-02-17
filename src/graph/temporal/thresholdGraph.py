from graph.ratingGraph import DEFAULT_GEN
from graph.temporal.ratingGraph import TemporalRatingGraph

import numpy as np
import random

DEFAULT_THRESHOLD = 0.5
DEFAULT_REMOVE_NON_VOTED = False
DEFAULT_Q = 0.5
DEFAULT_PAY = 1.0

class ThresholdGraph(TemporalRatingGraph):

    def __init__(self, bribers, generator=DEFAULT_GEN, **kwargs):
        super().__init__(bribers, generator=generator, **kwargs)

        # Initialise parameters of threshold graph
        # - thresh - threshold for being considered
        # - rm_no_vote - whether to allow non voted restaurants
        # - q - percentage of max rating given to non voted restaurants
        if "threshold" in kwargs.keys():
            self.thresh = kwargs["threshold"]
        else:
            self.thresh = DEFAULT_THRESHOLD
        if "remove_non_voted" in kwargs.keys():
            self.rm_no_vote = kwargs["remove_non_voted"]
        else:
            self.rm_no_vote = DEFAULT_REMOVE_NON_VOTED
        if "q" in kwargs.keys():
            self.q = kwargs["q"] * self._max_rating
        else:
            self.q = DEFAULT_Q * self._max_rating
        if "pay" in kwargs.keys():
            self.pay = kwargs["pay"]
        else:
            self.pay = DEFAULT_PAY

    def _customer_action(self):

        # obtain customers ratings before any actions at this step
        # assumes all customers act simultaneously
        curr_ratings = [
            [self.get_rating(n, b) for b in self.get_bribers()]
                for n in self._g.nodes]
        voted = [
            [len(self._neighbours(n, b)) > 0 for b in self.get_bribers()]
                for n in self._g.nodes]

        # for each customer
        for n in self._g.nodes():
            # get weightings for restaurants
            # 0 if below_threshold, q if no votes
            weights = np.zeroes(len(self._bribers))

            for b in range(0, len(self._bribers)):
                # Check for no votes
                if not voted[n][b]:
                    if self.rm_no_vote:
                        weights[b] = 0
                    else:
                        weights[b] = self.q
                # P-rating below threshold
                elif curr_ratings[n][b] < self.thresh:
                    weights[b] = 0;
                # Else probability proportional to P-rating
                else:
                    weights[b] = curr_ratings[n][b]

            # no restaurants above threshold so no action
            if np.count_nonzero(weights) == 0:
                return

            # select at random
            selected = random.choices(range(0, len(bribers)), weights=weights)

            # act on selection
            if self._votes[n][selected] == np.NaN: # no previous vote/ bribe
                self._votes[n][selected] = self._truths[n][selected]

            self._bribers[selected].add_resources(self.pay)
