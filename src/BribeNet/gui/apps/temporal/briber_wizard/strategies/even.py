import tkinter as tk

from BribeNet.gui.classes.param_list_frame import ParamListFrame


class EvenFrame(ParamListFrame):
    name = "Even"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'u_0': tk.DoubleVar(self, value=10)
        }

        self.descriptions = {
            'u_0': 'starting budget'
        }

        self.grid_params(show_name=False)
