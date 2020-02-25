from graph.ratingGraph import DEFAULT_GEN
from graph.temporal.action.customerAction import CustomerAction
from graph.temporal.ratingGraph import TemporalRatingGraph


class NoCustomerActionGraph(TemporalRatingGraph):
    """
    A temporal rating graph solely for testing purposes.
    """

    def __init__(self, bribers, generator=DEFAULT_GEN, **kwargs):
        super().__init__(bribers, generator=generator, **kwargs)

    def _customer_action(self):
        return CustomerAction(self)
