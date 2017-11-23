# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 23:36:47 2014

@author: rishu
"""

import TweetDB as TDB
#import EpiPipesApi as epi
from EpiPipesApi import *
from graph_tool.all import *
import graph_tool.topology as gt
import matplotlib


id_to_vertex = {}

#mentions_recs = scan(TDB.session, limit(TDB.session, TDB.Network, 100000))
mentions_recs = scan(TDB.session, TDB.Network)
g = Graph()
a = set()
for erec in mentions_recs:
    #print erec.src_id, " ", erec.des_id
    if erec.src_id not in id_to_vertex.keys():
        id_to_vertex[erec.src_id] = g.add_vertex()
    if erec.des_id not in id_to_vertex.keys():
        id_to_vertex[erec.des_id]  = g.add_vertex()
    g.add_edge(id_to_vertex[erec.src_id], id_to_vertex[erec.des_id])
#l = gt.label_largest_component(g)
#u = gt.GraphView(g, vfilt=l)
#print "Connected Component Size:", u.num_vertices(), u.num_edges()
pos = sfdp_layout(g)  #sfdp_layout(l)
graph_draw(g, pos, output_size=(1000, 1000), vertex_color=[1,1,1,0],
            vertex_size=1, edge_pen_width=1.2,
           vcmap=matplotlib.cm.gist_heat_r, output="full_graph.png")