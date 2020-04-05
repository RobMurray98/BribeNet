from gui.apps.static.wizard.algos.algo_frame import GeneratorAlgoFrame
import tkinter as tk


class WattsStrogatz(GeneratorAlgoFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Watts-Strogatz"

        self.params = {
            'n': tk.IntVar(self, value=30),
            'neighbours': tk.IntVar(self, value=5),
            'p': tk.DoubleVar(self, value=0.3)
        }

        for i, (name, var) in enumerate(self.params.values()):
            label = tk.Label(text=name)
            label.grid(row=i, column=0)
            tk.Entry(self, textvariable=var).grid(row=i, column=1)