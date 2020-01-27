#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 20:36:51 2019
@author: callum
"""

# Import Bribing Agents
from bribery.static.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from bribery.static.oneMoveRandomBriber import OneMoveRandomBriber

from graph.static.ratingGraph import StaticRatingGraph

import tkinter as tk
import networkit as nk
from networkx import spring_layout
from networkit.nxadapter import nk2nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from networkit.viztasks import drawGraph
from matplotlib.colors import rgb2hex


def switch_briber(argument):
    switcher = {
        "r": lambda: OneMoveRandomBriber(10),
        "i": lambda: OneMoveInfluentialNodeBriber(10)
    }
    return switcher.get(argument)


# outer layer of application
# links start page with graph page
class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in [StartPage, GraphFrame, ResultsFrame]:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def generate_graph(self, gtype, btype):
        briber = switch_briber(btype)()
        # noinspection PyUnresolvedReferences
        ba_gen = nk.generators.BarabasiAlbertGenerator(5, 30, 0, True)
        rg = StaticRatingGraph(briber) if gtype == "ws" else StaticRatingGraph(briber, generator=ba_gen)
        self.frames["GraphFrame"].set_graph(rg, briber)

    def plot_results(self, results):
        self.frames["ResultsFrame"].plot_results(results)


# page for selection of graph and bribery method
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        gtype = tk.StringVar()
        gtype.set("L")
        btype = tk.StringVar()
        btype.set("L")

        rb1 = tk.Radiobutton(self, variable=gtype, value="ws", text="Watts-Strogatz")
        rb2 = tk.Radiobutton(self, variable=gtype, value="ba", text="Barabási–Albert")
        rb1.grid(row=0, column=0)
        rb2.grid(row=1, column=0)

        rba = tk.Radiobutton(self, variable=btype, value="r", text="Random")
        rbb = tk.Radiobutton(self, variable=btype, value="i", text="Influential")
        rba.grid(row=0, column=1)
        rbb.grid(row=1, column=1)

        b = tk.Button(self, text="Graph + Test", command=lambda: self.on_button(gtype.get(), btype.get()))
        b.grid(row=1, column=2)

    def on_button(self, gtype, btype):
        self.controller.generate_graph(gtype, btype)
        self.controller.show_frame("GraphFrame")


# page for displaying and running graph
class GraphFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.results = []

        button1 = tk.Button(self, text="Exit", command=lambda: self.controller.show_frame("StartPage"))
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
        self.controller.show_frame("ResultsFrame")

    def display_graph(self, last=-1):

        cmap = plt.get_cmap("Purples")
        colors = []
        for c in self.graph.get_customers():
            if not self.graph.get_vote(c):
                colors.append("gray")
            else:
                colors.append(rgb2hex(cmap(self.graph.get_vote(c)[0])[:3]))
        # labels = {c: round(self.graph.p_rating(c), 2) for c in self.graph.get_customers()}

        self.ax.clear()

        drawGraph(self.graph.graph(), node_size=400, node_color=colors, ax=self.ax, pos=self.pos)
        for c in self.graph.get_customers():
            if not self.graph.get_vote(c):
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
        if last >= 0:
            self.ax.add_artist(plt.Circle(
                (self.pos[last][0], self.pos[last][1]), 0.1,
                color="r",
                fill=False,
                linewidth=3.0
            ))
        self.canvas.draw()
        avp = str(round(self.graph.eval_graph(), 2))
        if last < 0:
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
            elif not self.graph.get_vote(c):
                colors.append("gray")
            else:
                colors.append(rgb2hex(cmap(self.graph.get_vote(c)[0])[:3]))
        self.ax.clear()

        for c in self.graph.get_customers():
            rating = ""
            if not self.graph.get_vote(c):
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
        self.ax.plot(xs, results)
        self.ax.set_xlabel("Moves over time")
        self.ax.set_ylabel("Average P-rating")
        self.canvas.draw()

    def exit(self):
        self.results = []
        self.controller.show_frame("StartPage")


if __name__ == '__main__':
    app = GUI()
    app.mainloop()
