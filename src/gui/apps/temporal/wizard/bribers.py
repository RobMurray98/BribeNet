import tkinter as tk


class TemporalBribers(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.bribers_txt = tk.StringVar(parent, value="")
        bribers_title_label = tk.Label(self, text="BRIBERS\n------")
        bribers_title_label.grid(row=12, column=4)
        bribers_text_label = tk.Label(self, textvariable=self.bribers_txt)
        bribers_text_label.grid(row=13, column=4)

        briber_ns = ["random", "influential", "non", "even"]
        briber_var = tk.StringVar(parent, value="random")

        select_bribers_label = tk.Label(self, text="SELECT BRIBERS\n------")
        select_bribers_label.grid(row=0, column=4)

        briber_menu = tk.OptionMenu(self, briber_var, *briber_ns)
        briber_menu.grid(row=1, column=4)

        u0_var = tk.DoubleVar(parent, value=10)
        u0_label = tk.Label(self, text="u0 (starting money)")
        u0_label.grid(row=3, column=3)
        u0_entry = tk.Entry(self, textvariable=u0_var)
        u0_entry.grid(row=3, column=4)

        add_briber = tk.Button(self, text="add", command=lambda: parent.add_briber(briber_var.get(), u0_var.get()))
        add_briber.grid(row=5, column=4)
