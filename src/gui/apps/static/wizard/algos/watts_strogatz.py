import tkinter as tk

from gui.classes.param_list_frame import ParamListFrame


class WattsStrogatz(ParamListFrame):
    name = "Watts-Strogatz"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'n_nodes': tk.IntVar(self, value=30),
            'n_neighbours': tk.IntVar(self, value=5),
            'p': tk.DoubleVar(self, value=0.3)
        }

        self.descriptions = {
            'n_nodes': 'number of nodes in the graph',
            'n_neighbours': 'number of neighbors on each side of a node',
            'p': 'the probability of rewiring a given edge'
        }

        self.grid_params(show_name=False)
