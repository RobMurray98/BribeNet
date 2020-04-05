import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from networkx import spring_layout
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb2hex
from networkit.nxadapter import nk2nx
from networkit.viztasks import drawGraph
from networkx import spring_layout
import numpy as np


class GraphFrame(tk.Frame):
    """
    Frame for showing the current state and actions that can be taken for the static model being run
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.results = []

        button1 = tk.Button(self, text="Exit", command=lambda: self.controller.show_subframe("WizardFrame"))
        button1.pack()

        button2 = tk.Button(self, text="Show Influential Nodes", command=lambda: self.show_influential())
        button2.pack()

        button3 = tk.Button(self, text="Bribe", command=lambda: self.next_bribe())
        button3.pack()

        button4 = tk.Button(self, text="Results", command=lambda: self.to_results())
        button4.pack()

        self.txt = tk.StringVar()
        lbl = tk.Label(self, textvariable=self.txt)
        lbl.pack()
        self.txt.set("Average P-Rating: -- \nLast Briber: --")

    def set_graph(self, graph, briber):
        self.graph = graph
        self.pos = spring_layout(nk2nx(self.graph.graph()))
        self.briber = briber
        self.results.append(self.graph.eval_graph())
        self.display_graph()

    def to_results(self):
        self.controller.plot_results(self.results)
        self.results = []
        self.controller.show_subframe("ResultsFrame")

    def display_graph(self, last=None):

        cmap = plt.get_cmap("Purples")
        colors = []
        for c in self.graph.get_customers():
            if np.isnan(self.graph.get_vote(c)):
                colors.append("gray")
            else:
                colors.append(rgb2hex(cmap(self.graph.get_vote(c)[0])[:3]))
        # labels = {c: round(self.graph.p_rating(c), 2) for c in self.graph.get_customers()}

        self.ax.clear()

        drawGraph(self.graph.graph(), node_size=400, node_color=colors, ax=self.ax, pos=self.pos)
        for c in self.graph.get_customers():
            if np.isnan(self.graph.get_vote(c)):
                rating = "None"
            else:
                rating = round(self.graph.get_vote(c)[0], 2)

            self.ax.annotate(
                str(c) + ":\n" +
                "Rating: " + str(rating) + "\n" +
                "PRating: " + str(round(self.graph.get_rating(c), 2)),
                xy=(self.pos[c][0], self.pos[c][1]),
                bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
            )
        if last is not None:
            self.ax.add_artist(plt.Circle(
                (self.pos[last][0], self.pos[last][1]), 0.1,
                color="r",
                fill=False,
                linewidth=3.0
            ))
        self.canvas.draw()
        avp = str(round(self.graph.eval_graph(), 2))
        if last is not None:
            self.txt.set("Average P-Rating: " + avp + " \nLast Bribed: --")
        else:
            self.txt.set("Average P-Rating: " + avp + " \nLast Bribed: " + str(last))

    def next_bribe(self):
        c = self.briber.next_bribe()
        self.display_graph(last=c)
        avp = self.graph.eval_graph()
        self.results.append(avp)
        self.canvas.draw()

    def show_influential(self):
        cmap = plt.get_cmap("Purples")
        colors = []

        for c in self.graph.get_customers():
            if self.graph.is_influential(c, charge_briber=False):
                colors.append("yellow")
            elif np.isnan(self.graph.get_vote(c)):
                colors.append("gray")
            else:
                colors.append(rgb2hex(cmap(self.graph.get_vote(c)[0])[:3]))
        self.ax.clear()

        for c in self.graph.get_customers():
            rating = ""
            if np.isnan(self.graph.get_vote(c)):
                rating = "None"
            else:
                rating = round(self.graph.get_vote(c)[0], 2)

            self.ax.annotate(
                str(c) + ":\n" +
                "Rating: " + str(rating) + "\n" +
                "PRating: " + str(round(self.graph.get_rating(c), 2)),
                xy=(self.pos[c][0], self.pos[c][1]),
                bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
            )
        drawGraph(self.graph.graph(), node_size=500, node_color=colors, ax=self.ax, pos=self.pos)
        self.canvas.draw()
