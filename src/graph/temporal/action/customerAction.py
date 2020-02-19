from typing import Dict, Any, Tuple, List

from bribery.temporal.action.briberyAction import BriberyAction
from graph.temporal.action.actionType import ActionType


class CustomerActionExecutedMultipleTimesException(Exception):
    pass


class CustomerActionTimeNotCorrectException(Exception):
    pass


class CustomerAction(object):

    def __init__(self, graph):

        from graph.temporal.ratingGraph import TemporalRatingGraph  # local import to remove cyclic dependency
        assert issubclass(graph.__class__, TemporalRatingGraph)
        self.graph = graph
        self._actions: Dict[int, Tuple[ActionType, Any]] = {c: (ActionType.NONE, None)
                                                            for c in self.graph.get_customers()}
        self.__time_step = self.graph.get_time_step()
        self.__performed = False

    def get_time_step(self):
        return self.__time_step

    def set_bribed(self, node_id: int, briber_ids: List[int]):
        self._actions[node_id] = (ActionType.BRIBED, briber_ids)

    def set_none(self, node_id: int):
        self._actions[node_id] = (ActionType.NONE, 0)

    def set_select(self, node_id: int, briber_id):
        self._actions[node_id] = (ActionType.SELECT, briber_id)

    def set_bribed_from_bribery_action(self, bribery_action: BriberyAction):
        for c in self._actions:
            bribed, bribers = bribery_action.is_bribed(c)
            if bribed:
                self.set_bribed(c, bribers)

    def perform_action(self):
        """
        Perform the described action on the graph
        """
        if not self.__performed:
            if self.__time_step == self.graph.get_time_step():
                for c in self._actions:
                    if self._actions[c] == ActionType.SELECT:
                        pass  # TODO
                self.__performed = True
            else:
                message = f"The time step of the TemporalRatingGraph ({self.graph.get_time_step()}) is not equal to " \
                          f"the intended execution time ({self.__time_step})"
                raise CustomerActionTimeNotCorrectException(message)
        else:
            raise CustomerActionExecutedMultipleTimesException()
