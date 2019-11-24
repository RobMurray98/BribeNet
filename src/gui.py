#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 20:36:51 2019

@author: callum
"""

from bribery.influentialNode import InfluentialNodeBriber
from bribery.mostInfluencialNode import MostInfluentialNodeBriber
from bribery.random import RandomBriber
from graphGenerator import RatingGraph
from parameterPrediction import test_parameter_prediction
import tkinter as tk
import networkit as nk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from networkit.viztasks import drawGraph

rating_graph = RatingGraph()
ba_gen = nk.generators.BarabasiAlbertGenerator(5,30,0,True)
rating_graph2 = RatingGraph(ba_gen)

#we need to find k in BA generator (here set to 5)
#it's definitely related to minimum degree of all nodes
#however, it's not just that simple
#clearly there's some kind of probability being used here
#my current best guess is a dynamic probability (equivalent for all nodes)
#such that the expected number of edges added when the node joins the graph =k
#hence greater than (roughly double?) the minimum degree of the final graph
for n in rating_graph2.graph().nodes():
    print(n, ":",rating_graph2.graph().degree(n))

def generate_graph(gtype, btype):
    # print(gtype)
    # print(btype)
    if gtype == "ba":
        briber_setup = switch_briber(btype)
        print("Testing selected bribery method on chosen graph type!")
        graph_and_test(briber_setup, rating_graph2.copy())
        return
    briber_setup = switch_briber(btype)
    print("Testing selected bribery method on chosen graph type!")
    graph = graph_and_test(briber_setup, rating_graph.copy())
    show_graph(graph)


def switch_briber(argument):
    switcher = {
        "r": lambda g: RandomBriber(g, 10),
        "i": lambda g: InfluentialNodeBriber(g, 10, 0.2),
        "mi": lambda g: MostInfluentialNodeBriber(g, 10, 0.2)
    }
    return switcher.get(argument)


def graph_and_test(briber_setup, graph):
    print(graph.eval_graph())
    print("Bribing!")
    briber = briber_setup(graph)
    briber.next_bribe()
    print(graph.eval_graph())
    print("")
    return graph


root = tk.Tk()

v = tk.StringVar()
v.set("L")

v2 = tk.StringVar()
v2.set("L")

rb1 = tk.Radiobutton(root, variable=v, value="ws", text="Watts-Strogatz")
rb2 = tk.Radiobutton(root, variable=v, value="ba", text="Barabási–Albert")
rb1.grid(row=0, column=0)
rb2.grid(row=1, column=0)

rba = tk.Radiobutton(root, variable=v2, value="r", text="Random")
rbb = tk.Radiobutton(root, variable=v2, value="i", text="Influential")
rbc = tk.Radiobutton(root, variable=v2, value="mi", text="MostInfluential")
rba.grid(row=0, column=1)
rbb.grid(row=1, column=1)
rbc.grid(row=2, column=1)

b = tk.Button(root, text="Graph + Test", command=lambda: generate_graph(v.get(), v2.get()))
b.grid(row=1, column=2)

def show_graph(graph):
    # subwind = tk.Toplevel()
    # fig = Figure(figsize=(5,5))
    drawGraph(graph.graph())
    plt.show()
    # canvas = FigureCanvasTkAgg(fig, subwind)
    # canvas.draw()
    # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

root.mainloop()
