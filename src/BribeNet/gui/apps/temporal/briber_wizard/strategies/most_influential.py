import tkinter as tk

from BribeNet.gui.classes.param_list_frame import ParamListFrame


class MostInfluentialFrame(ParamListFrame):
    name = "Most Influential"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'u_0': tk.DoubleVar(self, value=10),
            'k': tk.DoubleVar(self, value=0.1),
            'i': tk.IntVar(self, value=7),
            'true_average': tk.DoubleVar(self, value=0.5),
            'true_std_dev': tk.DoubleVar(self, value=0.2)
        }

        self.descriptions = {
            'u_0': 'starting budget',
            'k': 'cost of information',
            'i': 'the number of bribery rounds to try to find the most influential node during',
            'true_average': 'the average of customer ground truth for this briber',
            'true_std_dev': 'the standard deviation of customer ground truth for this briber'
        }

        self.grid_params(show_name=False)
