import tkinter as tk

from gui.classes.param_list_frame import ParamListFrame


class InfluentialFrame(ParamListFrame):
    name = "Influential"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'u_0': tk.DoubleVar(self, value=10),
            'k': tk.DoubleVar(self, value=0.1)
        }

        self.descriptions = {
            'u_0': 'starting budget',
            'k': 'cost of information'
        }

        self.grid_params()
