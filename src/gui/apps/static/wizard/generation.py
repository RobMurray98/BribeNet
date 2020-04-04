import tkinter as tk


class StaticGeneration(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.gtype = tk.StringVar(parent)
        self.gtype.set("L")


        tk.Label(self, text="SELECT GRAPH GENERATOR\n------").grid(row=0, column=0)

        rb1 = tk.Radiobutton(self, variable=self.gtype, value="ws", text="Watts-Strogatz")
        self.arg1_vars = [tk.IntVar(parent, value=30), tk.IntVar(parent, value=5), tk.DoubleVar(parent, value=0.3)]
        arg1_lbls = [
            tk.Label(self, text="n_nodes"),
            tk.Label(self, text="n_neighbours"),
            tk.Label(self, text="p"),
        ]
        rb1.grid(row=1, column=0)
        for i, a in enumerate(arg1_lbls):
            a.grid(row=2, column=i)
        for i, a in enumerate(self.arg1_vars):
            tk.Entry(self, textvariable=a).grid(row=3, column=i)

        rb2 = tk.Radiobutton(self, variable=self.gtype, value="ba", text="Barabási–Albert")
        self.arg2_vars = [tk.IntVar(parent, value=5), tk.IntVar(parent, value=30), tk.IntVar(parent, value=0)]
        arg2_lbls = [
            tk.Label(self, text="k"),
            tk.Label(self, text="n_max"),
            tk.Label(self, text="n0"),
        ]
        rb2.grid(row=4, column=0)
        for i, a in enumerate(arg2_lbls):
            a.grid(row=5, column=i)
        for i, a in enumerate(self.arg2_vars):
            tk.Entry(self, textvariable=a).grid(row=6, column=i)

        rb3 = tk.Radiobutton(self, variable=self.gtype, value="cg", text="Composite Generator")
        self.arg3_vars = [tk.IntVar(parent, value=50), tk.IntVar(parent, value=5), tk.IntVar(parent, value=2),
                          tk.DoubleVar(parent, value=0.1), tk.IntVar(parent, value=3), tk.DoubleVar(parent, value=0.05)]
        arg3_lbls = [
            tk.Label(self, text="n_nodes"),
            tk.Label(self, text="community_count"),
            tk.Label(self, text="small_world_neighbours"),
            tk.Label(self, text="rewiring_prob"),
            tk.Label(self, text="scale_free_k"),
            tk.Label(self, text="probability_reduce"),
        ]
        rb3.grid(row=7, column=0)
        for i, a in enumerate(arg3_lbls):
            a.grid(row=8, column=i)
        for i, a in enumerate(self.arg3_vars):
            tk.Entry(self, textvariable=a).grid(row=9, column=i)