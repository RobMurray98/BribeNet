import tkinter as tk

from gui.classes.param_list_frame import ParamListFrame


class MostInfluentialFrame(ParamListFrame):
    name = "Most Influential"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'u_0': tk.DoubleVar(self, value=10),
            'k': tk.DoubleVar(self, value=0.1),
            'i': tk.IntVar(self, value=7)
        }

        self.descriptions = {
            'u_0': 'starting budget',
            'k': 'cost of information',
            'i': 'the number of bribery rounds to try to find the most influential node during'
        }

        self.grid_params(show_name=False)
