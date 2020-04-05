from gui.apps.static.wizard.algos.algo_frame import GeneratorAlgoFrame
import tkinter as tk


class Composite(GeneratorAlgoFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Composite"

        self.params = {
            'n': tk.IntVar(self, value=50),
            'communities': tk.IntVar(parent, value=5),
            'neighbours': tk.IntVar(self, value=2),
            'p': tk.DoubleVar(self, value=0.3),
            'k': tk.IntVar(parent, value=3),
            'p_reduce': tk.DoubleVar(parent, value=0.05)
        }

        for i, (name, var) in enumerate(self.params.values()):
            label = tk.Label(text=name)
            label.grid(row=i, column=0)
            tk.Entry(self, textvariable=var).grid(row=i, column=1)
