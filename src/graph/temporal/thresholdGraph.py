from graph.ratingGraph import DEFAULT_GEN
from graph.temporal.ratingGraph import TemporalRatingGraph


class ThresholdGraph(TemporalRatingGraph):

    def __init__(self, bribers, generator=DEFAULT_GEN, **kwargs):
        super().__init__(bribers, generator=generator, **kwargs)

    def _customer_action(self):
        # TODO (i30): implement threshold model customer logic
        raise NotImplementedError
