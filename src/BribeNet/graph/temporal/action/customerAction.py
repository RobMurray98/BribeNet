from typing import Dict, Any, Tuple, List

import numpy as np

from BribeNet.bribery.temporal.action.briberyAction import BriberyAction
from BribeNet.bribery.temporal.briber import GraphNotSubclassOfTemporalRatingGraphException
from BribeNet.graph.temporal.action.actionType import ActionType
from BribeNet.helpers.bribeNetException import BribeNetException


class CustomerActionExecutedMultipleTimesException(BribeNetException):
    pass


class CustomerActionTimeNotCorrectException(BribeNetException):
    pass


class CustomerAction(object):

    def __init__(self, graph):
        from BribeNet.graph.temporal.ratingGraph import TemporalRatingGraph  # local import to remove cyclic dependency
        if not issubclass(graph.__class__, TemporalRatingGraph):
            raise GraphNotSubclassOfTemporalRatingGraphException(f"{graph.__class__.__name__} is not a subclass of "
                                                                 "TemporalRatingGraph")
        self.graph = graph
        self.actions: Dict[int, Tuple[ActionType, Any]] = {c: (ActionType.NONE, None)
                                                           for c in self.graph.get_customers()}
        self.__time_step = self.graph.get_time_step()
        self.__performed = False

    @classmethod
    def empty_action(cls, graph):
        return cls(graph)

    def get_time_step(self):
        return self.__time_step

    def get_performed(self):
        return self.__performed

    def get_action_type(self, node_id: int):
        return self.actions[node_id][0]

    def set_bribed(self, node_id: int, briber_ids: List[int]):
        self.actions[node_id] = (ActionType.BRIBED, briber_ids)

    def set_none(self, node_id: int):
        self.actions[node_id] = (ActionType.NONE, 0)

    def set_select(self, node_id: int, briber_id):
        self.actions[node_id] = (ActionType.SELECT, briber_id)

    def set_bribed_from_bribery_action(self, bribery_action: BriberyAction):
        for c in self.actions:
            bribed, bribers = bribery_action.is_bribed(c)
            if bribed:
                self.set_bribed(c, bribers)

    # noinspection PyProtectedMember
    def perform_action(self, pay: float):
        """
        Perform the described action on the graph
        :param pay: the amount to increase a selected briber's utility
        """
        if not self.__performed:
            if self.__time_step == self.graph.get_time_step():
                for c in self.actions:
                    if self.actions[c][0] == ActionType.SELECT:
                        selected = self.actions[c][1]
                        if np.isnan(self.graph._votes[c][selected]):  # no previous vote or bribe
                            self.graph._votes[c][selected] = self.graph._truths[c][selected]
                        self.graph._bribers[selected].add_resources(pay)
                self.__performed = True
            else:
                message = f"The time step of the TemporalRatingGraph ({self.graph.get_time_step()}) is not equal to " \
                          f"the intended execution time ({self.__time_step})"
                raise CustomerActionTimeNotCorrectException(message)
        else:
            raise CustomerActionExecutedMultipleTimesException()
