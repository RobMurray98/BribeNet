import tkinter as tk


class Main(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master=master, *args, **kwargs)
        static_button = tk.Button(self, text="Static Model", command=self.master.show_static_gui)
        static_button.pack()
        temporal_button = tk.Button(self, text="Temporal Model", command=self.master.show_temporal_gui)
        temporal_button.pack()
