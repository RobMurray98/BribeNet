#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 21:04:19 2019

@author: callum
"""

import networkx as nx
import matplotlib as plt
import random
    
# Basic file open method
# Tested only facebook, but format should be consistent for SNAP datasets
f = open("data/facebook/facebook_combined.txt","rt")

# Split each line on space char and remove trailing newline
edges = []
for line in f:
    edges.append(line[:len(line)-1].split(" "))

facebook = nx.Graph(edges)