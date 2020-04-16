import tkinter as tk

from gui.apps.temporal.briber_wizard.strategies.strategy_frame import StrategyFrame


class EvenFrame(StrategyFrame):
    name = "Even"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'u_0': tk.DoubleVar(self, value=10)
        }

        for i, (name, var) in enumerate(self.params.items()):
            label = tk.Label(self, text=name)
            label.grid(row=i, column=0)
            entry = tk.Entry(self, textvariable=var)
            entry.grid(row=i, column=1)
