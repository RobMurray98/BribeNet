from gui.apps.static.wizard.algos.algo_frame import GeneratorAlgoFrame
import tkinter as tk


class BarabasiAlbert(GeneratorAlgoFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Barabási-Albert"

        self.params = {
            'n': tk.IntVar(self, value=30),
            'n_0': tk.IntVar(self, value=0),
            'k': tk.DoubleVar(self, value=5)
        }

        for i, (name, var) in enumerate(self.params.items()):
            label = tk.Label(text=name)
            label.grid(row=i, column=0)
            tk.Entry(self, textvariable=var).grid(row=i, column=1)
