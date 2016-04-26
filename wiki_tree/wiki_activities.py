# -*- coding: utf-8 -*-

import networkx as nx
import pickle
from wikitools import wiki
from wikitools import page
from wikitools import category

site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

with open('objs.pickle') as f:
    G, lst, level, id = pickle.load(f)

# Reverse graph to get faster results
G_rev = G.reverse()

def get_paths(act):
    pg = page.Page(site, act)
    cat = pg.getCategories()
    
    cat_ = []
    path_ = []
    set_ = []
    for c in cat:
        c = c[9:]
        if c in G:
            cat_.append(c)
            p = nx.dijkstra_path(G_rev, c, root)
            path_.append(p)
            s = set(p)
            set_.append(s)
        
    return [cat_, path_, set_]    

def score(depth):
    return depth

def find_best_common_path(act, act2):
    [cat_, path_, set_] = get_paths(act)
    [cat2_, path2_, set2_] = get_paths(act2)
    curr_max = score(0)
    curr_pair = [0, 0]
    for i in range(len(set_)):
        for j in range(len(set2_)):
            common = set_[i].intersection(set2_[j])
            #print common
            depth = len(common)
            #print depth
            scor = score(depth)
            if(scor > curr_max):
                curr_max = scor
                curr_pair = [i, j]
    
    return [curr_max, path_[curr_pair[0]], path2_[curr_pair[1]]]

root = 'Main topic classifications'

act_pair = [
'Archery ',
'Shooting sport'
]

[cat1, path1, set1] = get_paths(act_pair[0])
[cat2, path2, set2] = get_paths(act_pair[1])

[scor, p, p2] = find_best_common_path(act_pair[0], act_pair[1])
