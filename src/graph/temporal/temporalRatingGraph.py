import abc

from graph.ratingGraph import RatingGraph, DEFAULT_GEN


class TemporalRatingGraph(RatingGraph, abc.ABC):

    def __init__(self, generator=DEFAULT_GEN, specifics=None, **kwargs):
        super().__init__(generator=generator, specifics=specifics, **kwargs)

    @abc.abstractmethod
    def step(self):
        """
        Defines the temporal model behaviour of the graph in a single time step.
        This should first determine the bribes to be carried out by querying
        instances of classes inheriting TemporalBriber for their action.
        Then simultaneously carries out the actions of bribed and non-bribed customers.
        """
        raise NotImplementedError