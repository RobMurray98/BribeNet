import tkinter as tk


class TemporalSettings(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        graph_lbls = [
            tk.Label(self, text="Threshold"),
            tk.Label(self, text="D (num bribe rounds)"),
            tk.Label(self, text="Q"),
            tk.Label(self, text="Apathy"),
        ]
        self.graph_params = [
            tk.DoubleVar(parent, value=0.5),
            tk.IntVar(parent, value=2),
            tk.DoubleVar(parent, value=0.5),
            tk.DoubleVar(parent, value=0.0)
        ]
        for i, a in enumerate(graph_lbls):
            a.grid(row=(i + 11), column=0)
        for i, a in enumerate(self.graph_params):
            entry = tk.Entry(self, textvariable=a)
            entry.grid(row=(i + 11), column=1)

    def get_graph_params(self):
        return [x.get() for x in self.graph_params]
