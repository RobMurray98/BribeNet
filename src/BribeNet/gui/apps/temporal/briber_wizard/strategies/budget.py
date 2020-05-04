import tkinter as tk

from BribeNet.gui.classes.param_list_frame import ParamListFrame


class BudgetFrame(ParamListFrame):
    name = "Budget"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'u_0': tk.DoubleVar(self, value=10),
            'k': tk.DoubleVar(self, value=0.1),
            'b': tk.DoubleVar(self, value=0.5)
        }

        self.descriptions = {
            'u_0': 'starting budget',
            'k': 'cost of information',
            'b': 'threshold of minimum potential increase in rating to fully bribe'
        }

        self.grid_params(show_name=False)
