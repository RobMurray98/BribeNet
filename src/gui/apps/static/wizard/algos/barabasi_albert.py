import tkinter as tk
from gui.apps.static.wizard.algos.algo_frame import GeneratorAlgoFrame


class BarabasiAlbert(GeneratorAlgoFrame):
    name = "Barabási-Albert"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'k': tk.DoubleVar(self, value=5),
            'n_max': tk.IntVar(self, value=30),
            'n_0': tk.IntVar(self, value=0)
        }

        self.descriptions = {
            'k': 'number of attachments per node',
            'n_max': 'number of nodes in the graph',
            'n_0': 'number of connected nodes to begin with'
        }

        self.grid_params()

