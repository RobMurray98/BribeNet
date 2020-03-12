import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb2hex
from networkit.nxadapter import nk2nx
from networkx import spring_layout
from networkit.viztasks import drawGraph


class GraphFrame(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=0)
        self.results = []

        button3 = tk.Button(self, text="Next Step", command=lambda: self.controller.next_step())
        button3.grid(row=3, column=2)

        button4 = tk.Button(self, text="Results", command=lambda: self.to_results())
        button4.grid(row=4, column=2)

        button1 = tk.Button(self, text="Exit", command=lambda: self.controller.show_frame("WizardFrame"))
        button1.grid(row=7, column=2)

        slide = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
        slide.grid(row=6,  column=2)
        button5 = tk.Button(self, text="Perform n steps", command=lambda: self.n_steps(slide.get()))
        button5.grid(row=5, column=2)

        self.info = tk.StringVar(parent)
        lbl = tk.Label(self, textvariable=self.info)
        lbl.grid(row=1, column=1, columnspan=2)
        self.info.set("--")

    def set_info(self, s):
        self.info.set(s)

    def set_pos(self, pos):
        self.pos = pos

    def n_steps(self, n):
        for i in range(0, n):
            self.controller.next_step()

    def add_briber_buttons(self, bribers):

        view_txt = tk.StringVar(self)
        lbl = tk.Label(self, textvariable=view_txt)
        lbl.grid(row=2, column=1)
        view_txt.set("View rating for briber")

        none_bt = tk.Button(self, text="none", command=lambda: self.draw_graph(self.controller.g, trust=1))
        none_bt.grid(row=3, column=1)

        print(self.controller)

        for i, c in enumerate(self.controller.bribers):

            bribe_bt = tk.Button(self, text=self.controller.briber_names[i], command=lambda i=i: self.draw_graph(self.controller.g, briber=i,
                                                                                          trust=1))
            bribe_bt.grid(row=(i+4), column=1)


    def to_results(self):
        self.controller.plot_results()
        self.controller.show_frame("ResultsFrame")

    def draw_graph(self, graph, **kwargs):

        colors = ["gray" for c in graph.get_customers()]
        if "briber" in kwargs:
            b = kwargs["briber"]

            # set colours for nodes
            cmap = plt.get_cmap("Purples")
            colors = []
            for c in graph.get_customers():
                if np.isnan(graph.get_vote(c)[b]):
                    colors.append("gray")
                else:
                    colors.append(rgb2hex(cmap(graph.get_vote(c)[b])[:3]))

        #default edges black
        edge_colors = ["#000000" for e in graph.get_edges()]

        # set colours for edges proportional to trust
        cmap2 = plt.get_cmap("Greys")
        if "trust" in kwargs and kwargs["trust"]:
            edge_colors = []
            for (u, v) in graph.get_edges():
                edge_colors.append(rgb2hex(cmap2(graph.get_weight(u, v))[:3]))

        self.ax.clear()

        drawGraph(
            graph.graph(),
            node_size=400,
            node_color=colors,
            edge_color=edge_colors,
            ax=self.ax, pos=self.pos,
            with_labels=True
        )

        if "briber" in kwargs:

            b = kwargs["briber"]

            # annotate votes on graph
            for c in graph.get_customers():
                if np.isnan(graph.get_vote(c)[b]):
                    rating = "None"
                else:
                    rating = round(graph.get_vote(c)[b], 2)

                self.ax.annotate(
                    str(c) + ":\n"
                    + "Vote: " + str(rating) + "\n"
                    + "PRating: " + str(round(graph.get_rating(c), 2)),
                    xy=(self.pos[c][0], self.pos[c][1]),
                    bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
                )

        # Show last bribe for bribers
        if "last" in kwargs:

            for n, c in zip(kwargs["last"], bribe_colors):
                self.ax.add_artist(plt.Circle(
                    (self.pos[n][0], self.pos[n][1]), 0.1,
                    color=c,
                    fill=False,
                    linewidth=3.0
                ))

        self.canvas.draw()

    # def show_influential(self):
    #     cmap = plt.get_cmap("Purples")
    #     colors = []
    #
    #     for c in self.graph.get_customers():
    #         if self.graph.is_influential(c, charge_briber=False):
    #             colors.append("yellow")
    #         elif np.isnan(self.graph.get_vote(c)):
    #             colors.append("gray")
    #         else:
    #             colors.append(rgb2hex(cmap(self.graph.get_vote(c)[0])[:3]))
    #     self.ax.clear()
    #
    #     for c in self.graph.get_customers():
    #         rating = ""
    #         if np.isnan(self.graph.get_vote(c)):
    #             rating = "None"
    #         else:
    #             rating = round(self.graph.get_vote(c)[0], 2)
    #
    #         self.ax.annotate(
    #             str(c) + ":\n" +
    #             "Rating: " + str(rating) + "\n" +
    #             "PRating: " + str(round(self.graph.get_rating(c), 2)),
    #             xy=(self.pos[c][0], self.pos[c][1]),
    #             bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    #         )
    #     drawGraph(self.graph.graph(), node_size=500, node_color=colors, ax=self.ax, pos=self.pos)
    #     self.canvas.draw()


class ResultsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        button1 = tk.Button(self, text="Exit", command=lambda: self.exit())
        button1.pack()

    def plot_results(self, results):
        xs = [i for i in range(0, len(results))]
        self.ax.clear()
        # for each briber
        for b in range(0, len(results[0])):
            ys = [r[b] for r in results]
            self.ax.plot(xs, ys, label=b)

        self.ax.set_xlabel("Moves over time")
        self.ax.set_ylabel("Average P-rating")
        self.ax.legend()
        self.canvas.draw()

    def exit(self):
        self.results = []
        self.controller.show_frame("GraphFrame")

