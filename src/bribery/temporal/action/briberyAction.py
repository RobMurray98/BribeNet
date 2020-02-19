from abc import ABC, abstractmethod
from typing import List


class BriberyActionExecutedMultipleTimesException(Exception):
    pass


class BriberyActionTimeNotCorrectException(Exception):
    pass


class BriberyAction(ABC):

    def __init__(self, graph):

        from graph.temporal.ratingGraph import TemporalRatingGraph  # local import to remove cyclic dependency
        assert issubclass(graph.__class__, TemporalRatingGraph)
        self.graph = graph
        self.__time_step = self.graph.get_time_step()
        self.__performed = False

    def perform_action(self):
        """
        Perform the action safely
        :raises BriberyActionTimeNotCorrectException: if action not at same time step as graph
        :raises BriberyActionExecutedMultipleTimesException: if action already executed
        """
        if not self.__performed:
            if self.__time_step == self.graph.get_time_step():
                self._perform_action()
                self.__performed = True
            else:
                message = f"The time step of the TemporalRatingGraph ({self.graph.get_time_step()}) is not equal to " \
                          f"the intended execution time ({self.__time_step})"
                raise BriberyActionTimeNotCorrectException(message)
        else:
            raise BriberyActionExecutedMultipleTimesException()

    def get_time_step(self):
        return self.__time_step

    @abstractmethod
    def _perform_action(self):
        """
        Perform the stored bribery actions simultaneously
        """
        raise NotImplementedError

    @abstractmethod
    def is_bribed(self, node_id) -> (bool, List[int]):
        """
        Determine if the bribery action results in a node being bribed this time step
        :param node_id: the node
        :return: whether the node is bribed this time step
        """
        raise NotImplementedError
