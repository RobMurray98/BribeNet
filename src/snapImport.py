#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from networkit.graphio import SNAPGraphReader

facebook = SNAPGraphReader().read("../data/facebook/facebook_combined.txt")
