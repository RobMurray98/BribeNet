import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ResultsFrame(tk.Frame):
    """
    Frame for showing the current results of the static model being run
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        button1 = tk.Button(self, text="Exit", command=self.exit)
        button1.pack()

    def plot_results(self, results):
        xs = [i for i in range(0, len(results))]
        self.ax.clear()
        self.ax.plot(xs, results)
        self.ax.set_xlabel("Moves over time")
        self.ax.set_ylabel("Average P-rating")
        self.canvas.draw()

    def exit(self):
        self.results = []
        self.master.show_frame("WizardFrame")
