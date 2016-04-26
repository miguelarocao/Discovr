# -*- coding: utf-8 -*-

import networkx as nx
import pickle
from wikitools import wiki
from wikitools import page
from wikitools import category

site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

with open('objs.pickle') as f:
    G, lst, level, id = pickle.load(f)

def get_paths(act1, act2):
    pg = page.Page(site, act)
    pg2 = page.Page(site, act2)
    
    cat = pg.getCategories()
    cat2 = pg2.getCategories()
    
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
    
    cat2_ = []
    path2_ = []
    set2_ = []
    for c in cat2:
        c = c[9:]
        if c in G:
            cat2_.append(c)
            p = nx.dijkstra_path(G_rev, c, root)
            path2_.append(p)
            s = set(p)
            set2_.append(s)
    
    return [cat_, cat2_, path_, path2_, set_, set2_]
    
def score(depth):
    return depth

def find_best_common_path(act, act2):
    [cat_, cat2_, path_, path2_, set_, set2_] = get_paths(act, act2)
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

# Reverse graph to get faster results
G_rev = G.reverse()

root = 'Main topic classifications'

act = 'Swimming (sport)'
act2 = 'Rafting'
act = 'Basketball'
act2 = 'American football'

#[cat, cat2, path, path2, set1, set2] = get_paths(act, act2)
[scor, p, p2] = find_best_common_path(act, act2)