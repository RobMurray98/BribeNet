import tkinter as tk

from BribeNet.gui.classes.param_list_frame import ParamListFrame


class TemporalSettings(ParamListFrame):
    name = 'Model Parameters'

    def __init__(self, parent):
        super().__init__(parent)

        self.descriptions = {
            'non_voter_proportion': 'the proportion of customers which start with no vote',
            'threshold': 'the minimum rating for a customer to consider visiting a bribing actor',
            'd': 'the period of non-bribery rounds (minimum 2)',
            'q': 'the vote value to use in place of non-votes in rating calculations',
            'pay': 'the amount of utility given to a bribing actor each time a customer chooses them',
            'apathy': 'the probability that a customer performs no action',
            'learning_rate': 'how quickly the edge weights are updated by trust'
        }

        self.params = {
            'non_voter_proportion': tk.DoubleVar(self, value=0.2),
            'threshold': tk.DoubleVar(self, value=0.5),
            'd': tk.IntVar(self, value=2),
            'q': tk.DoubleVar(self, value=0.5),
            'pay': tk.DoubleVar(self, value=1.0),
            'apathy': tk.DoubleVar(self, value=0.0),
            'learning_rate': tk.DoubleVar(self, value=0.1),
        }

        self.grid_params()
