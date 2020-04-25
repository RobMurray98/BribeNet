import tkinter as tk

from gui.classes.param_list_frame import ParamListFrame


class Composite(ParamListFrame):
    name = "Composite"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'n_nodes': tk.IntVar(self, value=50),
            'n_communities': tk.IntVar(self, value=5),
            'n_neighbours': tk.IntVar(self, value=2),
            'p_rewiring': tk.DoubleVar(self, value=0.3),
            'k': tk.DoubleVar(self, value=3),
            'p_reduce': tk.DoubleVar(self, value=0.05)
        }

        self.descriptions = {
            'n_nodes': 'number of nodes in the graph',
            'n_communities': 'how many small world networks the composite network should consist of',
            'n_neighbours': 'how many neighbours each node should have at the start of small world generation (k from '
                            'Watts-Strogatz)',
            'p_rewiring': 'the probability of rewiring a given edge during small world network generation (p from '
                          'Watts-Strogatz)',
            'k': 'number of attachments per community (k for Barabasi-Albert for our parent graph)',
            'p_reduce': "how much the probability of joining two nodes in two different communities is reduced by - "
                        "once a successful connection is made, the probability of connecting two edges p' becomes p' "
                        "* probability_reduce "
        }

        self.grid_params()
