import tkinter as tk

from gui.apps.temporal.briber_wizard.strategies.strategy_frame import StrategyFrame


class EvenFrame(StrategyFrame):
    name = "Even"

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'u_0': tk.DoubleVar(self, value=10)
        }

        self.descriptions = {
            'u_0': 'starting budget'
        }

        self.grid_params()
