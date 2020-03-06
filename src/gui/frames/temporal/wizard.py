import tkinter as tk


class WizardFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        gtype = tk.StringVar()
        gtype.set("L")
        btype = tk.StringVar()
        btype.set("L")

        tk.Label(self, text="SELECT GRAPH GENERATOR\n------").grid(row=0, column=0)

        rb1 = tk.Radiobutton(self, variable=gtype, value="ws", text="Watts-Strogatz")
        self.arg1_vars = [tk.IntVar(value=30), tk.IntVar(value=5), tk.DoubleVar(value=0.3)]
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

        rb2 = tk.Radiobutton(self, variable=gtype, value="ba", text="Barabási–Albert")
        self.arg2_vars = [tk.IntVar(value=5), tk.IntVar(value=30), tk.IntVar(value=0)]
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

        self.bribers_txt = tk.StringVar(value="")
        tk.Label(self, text="BRIBERS\n------").grid(row=12, column=4)
        tk.Label(self, textvariable=self.bribers_txt).grid(row=13, column=4)

        briber_ns = ["random", "influential", "non"]
        briber_var = tk.StringVar(value="random")

        tk.Label(self, text="SELECT BRIBERS\n------").grid(row=0, column=4)

        briber_menu = tk.OptionMenu(self, briber_var, *briber_ns)
        briber_menu.grid(row=1, column=4)

        u0_var = tk.DoubleVar(value=10)
        tk.Label(self, text="u0 (starting money)").grid(row=3, column=3)
        tk.Entry(self, textvariable=u0_var).grid(row=3, column=4)

        add_briber = tk.Button(self, text="add", command=lambda: self.add_briber(briber_var.get(), u0_var.get()))
        add_briber.grid(row=5, column=4)

        tk.Label(self, text="MODEL PARAMETERS\n------").grid(row=8, column=0)

        self.graph_params = [
            tk.DoubleVar(value=0.5),
            tk.IntVar(value=2),
            tk.DoubleVar(value=0.5),
            tk.DoubleVar(value=0.0)
        ]
        graph_lbls = [
            tk.Label(self, text="Threshold"),
            tk.Label(self, text="D (num bribe rounds)"),
            tk.Label(self, text="Q"),
            tk.Label(self, text="Apathy"),
        ]
        for i, a in enumerate(graph_lbls):
            a.grid(row=(i + 9), column=0)
        for i, a in enumerate(self.graph_params):
            tk.Entry(self, textvariable=a).grid(row=(i + 9), column=1)

        b = tk.Button(self, text="Graph + Test", command=lambda: self.on_button(gtype.get()))
        b.grid(row=8, column=5)

    def add_briber(self, b_type, u0):
        self.controller.add_briber(b_type, u0)
        txt = self.bribers_txt.get()
        txt += f"\n{b_type}: u0={u0}"
        self.bribers_txt.set(txt)

    def on_button(self, gtype):
        # check some bribers on graph
        if self.bribers_txt.get() == "":
            tk.messagebox.showerror(messgae="Graph needs one or more bribers")
            return

        args = []
        if gtype == "ws":
            args = [x.get() for x in self.arg1_vars]
        elif gtype == "ba":
            args = [x.get() for x in self.arg2_vars]

        params = [x.get() for x in self.graph_params]

        self.controller.add_graph(gtype, args, params)
        self.controller.show_frame("GraphFrame")
