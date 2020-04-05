import tkinter as tk


class WizardFrame(tk.Frame):
    """
    Frame for the wizard to construct a static model run
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        gtype = tk.StringVar(parent)
        gtype.set("L")
        btype = tk.StringVar(parent)
        btype.set("L")

        rb1 = tk.Radiobutton(self, variable=gtype, value="ws", text="Watts-Strogatz")
        rb2 = tk.Radiobutton(self, variable=gtype, value="ba", text="Barabási–Albert")
        rb3 = tk.Radiobutton(self, variable=gtype, value="cg", text="Composite Generator")
        rb1.grid(row=0, column=0)
        rb2.grid(row=1, column=0)
        rb3.grid(row=2, column=0)

        rba = tk.Radiobutton(self, variable=btype, value="r", text="Random")
        rbb = tk.Radiobutton(self, variable=btype, value="i", text="Influential")
        rba.grid(row=0, column=1)
        rbb.grid(row=1, column=1)

        b = tk.Button(self, text="Graph + Test", command=lambda: self.on_button(gtype.get(), btype.get()))
        b.grid(row=1, column=2)

    def on_button(self, gtype, btype):

        self.controller.generate_graph(gtype, btype)
        self.controller.show_subframe("GraphFrame")
