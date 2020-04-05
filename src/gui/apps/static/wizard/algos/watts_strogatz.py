from gui.apps.static.wizard.algos.algo_frame import GeneratorAlgoFrame
import tkinter as tk


class WattsStrogatz(GeneratorAlgoFrame):

    name = "Watts-Strogatz"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'n_nodes': tk.IntVar(self, value=30),
            'n_neighbours': tk.IntVar(self, value=5),
            'p': tk.DoubleVar(self, value=0.3)
        }

        for i, (name, var) in enumerate(self.params.items()):
            label = tk.Label(self, text=name)
            label.grid(row=i, column=0)
            entry = tk.Entry(self, textvariable=var)
            entry.grid(row=i, column=1)
