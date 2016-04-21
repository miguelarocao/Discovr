# -*- coding: utf-8 -*-

#import wikipedia as wiki
import json

import networkx as nx
import pickle

import pprint
import datetime
from wikitools import wiki
from wikitools import api
from wikitools import category
import wikitools
from wikitools import page
import re
from wikitools.page import NoPage

site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

#file1 = open('WCG.txt', 'w')
file_ex = open('WCG_ex.txt', 'w')

def add_cats(G, lst, level, id):
#    if len(lst) == id:
#        return
    try:
        src = lst[id]
        cat = category.Category(site, src)
        #catlist = cat.getAllMembers(namespaces=[14], titleonly=True)
        subcatlist = cat.getAllMembers(namespaces=[site.NS_CATEGORY], titleonly=True)

        for subcat in subcatlist:
            #remove 'Category:' from the string
            subcat = subcat[9:]
            if subcat not in G:
                #print "Adding category " + str(subcat)
                G.add_node(subcat)
                print "Id " + str(id) + " Size " + str(len(lst)) + " Level " + str(level[id]+1) + ": Adding edge from \'" + src + "\' to \'" + subcat + "\'"
                string = "Level " + str(level[id]+1) + ": \'" + src + "\' -> \'" + subcat + "\'\n"
                #file1.write(string.encode('utf8', 'replace'))
                G.add_edge(src, subcat)
                lst.append(subcat)
                level.append(level[id]+1)
                
    except Exception as ex:
#       if ex is NoPage:
#        log('main exception occurred! page not found='+ex.message)
        pprint.pprint(ex)
        string = str(ex) + "\n"
        file_ex.write(string.encode('utf8', 'replace'))
        #pass
    #add_cats(G, lst, level, id+1)
    return


G = nx.DiGraph()

#search = wiki.search("Ball games")
root = unicode("Main topic classifications")
#root = unicode("Dogs as pets")
#root = unicode("Health by country")
print "Adding source page \'" + root + "\'"
G.add_node(root)
string = "Level 0: \'" + root + "\'\n"
#file1.write(string.encode('utf8', 'replace'))

load = True

if load is False:
    lst = [root]
    level = [0]
    id = 0
else:
    # Getting back the objects:
    with open('objs.pickle') as f:
        G, lst, level, id = pickle.load(f)
    
while id < len(lst):
    if id%10000 is 0:
        # Saving the objects:
        with open('objs.pickle', 'w') as f:
            pickle.dump([G, lst, level, id], f)
    
    add_cats(G, lst, level, id)
    id += 1

# Saving the objects:
with open('objs.pickle', 'w') as f:
    pickle.dump([G, lst, level, id], f)

#pos=graphviz_layout(G,prog='dot')
#nx.draw_networkx(G)

#file2 = open('WCG_node_link_data.txt', 'w')

#data = json_graph.node_link_data(G)
#data = json_graph.node_link_data(G)
#json.dump(data, file2)

#file1.close()
file_ex.close()
#file2.close()
