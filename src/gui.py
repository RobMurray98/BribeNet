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

rating_graph = RatingGraph()

def buttonFunc(gtype, btype):
    #print(gtype)
    #print(btype)
    if gtype=="ba":
        print("not officially supported yet")
        return
    briber_setup = switch_briber(btype)
    print("Testing selected bribery method on chosen graph type!")
    graph_and_test(briber_setup, rating_graph.copy())
    

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

root = tk.Tk()

v = tk.StringVar()
v.set("L")

v2 = tk.StringVar()
v2.set("L")

rb1 = Radiobutton(root, variable=v, value="ws", text="Watts-Strogatz")
rb2 = Radiobutton(root, variable=v, value="ba", text="Barabási–Albert")
rb1.grid(row=0,column=0)
rb2.grid(row=1,column=0)

rba = Radiobutton(root, variable=v2, value="r", text="Random")
rbb = Radiobutton(root, variable=v2, value="i", text="Influential")
rbc = Radiobutton(root, variable=v2, value="mi", text="MostInfluential")
rba.grid(row=0,column=1)
rbb.grid(row=1,column=1)
rbc.grid(row=2,column=1)

b = Button(root, text="Graph + Test", command=lambda: buttonFunc(v.get(), v2.get()))
b.grid(row=1,column=2)

subwind = tk.Toplevel()
b2 = Button(subwind, text="I am a button", command=buttonFunc)
b2.pack(side=LEFT)

root.mainloop()