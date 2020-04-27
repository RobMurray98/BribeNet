import tkinter as tk

from gui.classes.param_list_frame import ParamListFrame


class TemporalSettings(ParamListFrame):
    name = 'Model Parameters'

    def __init__(self, parent):
        super().__init__(parent)

        self.descriptions = {
            'non_voter_proportion': 'the proportion of customers which start with no vote',
            'threshold': 'the minimum rating for a customer to consider visiting a bribing actor',
            'd': 'the period of non-bribery rounds (minimum 2)',
            'q': 'the vote value to use in place of non-votes in rating calculations',
            'apathy': 'the probability that a customer performs no action',
            'true_average': 'the average around which ground truths are distributed',
            'true_std_dev': 'the standard deviation by which ground truths are distributed'
        }

        self.params = {
            'non_voter_proportion': tk.DoubleVar(self, value=0.2),
            'threshold': tk.DoubleVar(self, value=0.5),
            'd': tk.IntVar(self, value=2),
            'q': tk.DoubleVar(self, value=0.5),
            'apathy': tk.DoubleVar(self, value=0.0),
            'true_average': tk.DoubleVar(self, value=0.5),
            'true_std_dev': tk.DoubleVar(self, value=0.2)
        }

        self.grid_params()
