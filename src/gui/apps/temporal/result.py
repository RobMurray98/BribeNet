import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ResultsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        exit_button = tk.Button(self, text="Exit", command=lambda: self.exit())
        exit_button.pack()

    def plot_results(self, results):
        xs = [i for i in range(0, len(results))]
        self.ax.clear()
        # for each briber
        for b in range(0, len(results[0])):
            ys = [r[b] for r in results]
            self.ax.plot(xs, ys, label=self.controller.briber_names[b])

        self.ax.set_xlabel("Moves over time")
        self.ax.set_ylabel("Average P-rating")
        self.ax.legend()
        self.canvas.draw()

    def exit(self):
        self.results = []
        self.controller.show_frame("GraphFrame")

