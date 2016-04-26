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

def score_depth(depth):
    return depth

def score_node_counts(node, node_counts):
    return 1.01**(-node_counts[node])

def find_best_common_path(act, act2, node_counts, use_counts):
    [cat_, path_, set_] = get_paths(act)
    [cat2_, path2_, set2_] = get_paths(act2)
    curr_max = 0
    for i in range(len(set_)):
        for j in range(len(set2_)):
            common = set_[i].intersection(set2_[j])
            #print common
            depth = len(common)
            #print depth
            if use_counts:
                scor = score_node_counts(path_[i][-depth], node_counts)
            else:
                scor = score_depth(depth)
            if(scor > curr_max):
                curr_max = scor
                curr_pair = [i, j]
    
    return [curr_max, path_[curr_pair[0]], path2_[curr_pair[1]]]

def gen_node_counts(acts):
    cats = dict()
    for elem in acts:
        [cat1, path1, set1] = get_paths(elem)
        for p in path1:
            for e in p:
                if e in cats:
                    cats[e] += 1
                else:
                    cats[e] = 1
    return cats
                
root = 'Main topic classifications'

acts = [
'Bowling',
'Dance',
'Disc Golf',
'Go Kart',
'Laser Tag',
'Mini Golf',
'Golf',
'Swimming (sport)',
'Salsa',
'Samba',
'Baseball',
'Basketball',
'Cricket',
'American football',
'Hockey',
'Rugby',
'Racquetball',
'Association football',
'Table Tennis',
'Tennis',
'Track and field',
'Running',
'Badminton',
'Curling',
'Boxing',
'Fitness',
'Sport Climbing',
'Rock Climbing',
'Cycling',
'Gymnastics',
'Martial Arts',
'Yoga',
'Paddleboarding',
'Field Hockey',
'Paintball',
'Rugby',
'Skateboarding',
'Inline skating',
'Roller skating',
'Skating',
'Squash',
'Surfing',
'Motorcycling',
'Hiking',
'Rafting',
'Skiing',
'Horseback Riding',
'Volleyball',
'Fencing',
'Parkour',
'Trampolining',
'Skydiving',
'Bungee jumping',
'Ziplining',
'Snowboarding',
'Softball',
'Archery ',
'Shooting sport',
'Racing',
'Billiards',
'Pool',
'Paragliding',
'Handball',
'Pottery',
'Photography',
'Painting',
'Drawing',
'Singing',
'Improv',
'Comedy',
'Theatre',
'Origami',
'Sculpture',
'Karaoke',
'Charity shop',
'Reading',
'Escape room',
'Gambling ',
'Arcade',
]

node_counts = gen_node_counts(acts)

act_pair = [
'Archery ',
'Shooting sport'
]

[cat1, path1, set1] = get_paths(act_pair[0])
[cat2, path2, set2] = get_paths(act_pair[1])

[scor, p, p2] = find_best_common_path(act_pair[0], act_pair[1], node_counts, True)