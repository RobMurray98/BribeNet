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

        for i, (name, var) in enumerate(self.params.items()):
            label = tk.Label(self, text=name)
            label.grid(row=i, column=0)
            entry = tk.Entry(self, textvariable=var)
            entry.grid(row=i, column=1)
