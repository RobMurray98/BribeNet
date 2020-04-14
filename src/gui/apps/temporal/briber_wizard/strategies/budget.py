import tkinter as tk

from gui.apps.temporal.briber_wizard.strategies.strategy_frame import StrategyFrame


class BudgetFrame(StrategyFrame):

    name = "Budget"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'u_0': tk.DoubleVar(self, value=10),
            'k': tk.DoubleVar(self, value=0.1),
            'b': tk.DoubleVar(self, value=0.5)
        }

        for i, (name, var) in enumerate(self.params.items()):
            label = tk.Label(self, text=name)
            label.grid(row=i, column=0)
            entry = tk.Entry(self, textvariable=var)
            entry.grid(row=i, column=1)
