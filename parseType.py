import itertools
import networkx as nx
from collections import Counter

def getCateTree():
    f = open('cate4sq.txt', 'r')
    lines = f.readlines()
    f.close()
    result = dict()
    i = 0
    curr = None
    listOfStacks = [[] for j in range(4)]
    while i < len(lines):
        line = lines[i]
        l = line.lstrip(' ')
        if l.startswith('Suggested Countries:'):
            i = i + 1
            continue
        space = len(line) - len(line.lstrip(' '))
        loc = space / 4
        if curr != None:
            if curr <= loc: # it move to right, subcategory
                listOfStacks[loc].append(l.strip('\n'))
            else: # it moves to left, end of subcategory
                index = len(listOfStacks[loc]) - 1 # the last element of stack
                for name in listOfStacks[curr]:
                    result[name] = listOfStacks[loc][index]
                listOfStacks[curr] = []
        i = i + 1
        curr = loc
        listOfStacks[loc].append(l.strip('\n'))
    return result

def getinitGraph(result):
    activity = result.keys()
    G=nx.Graph()
    for item in itertools.combinations(activity, 2):
        G.add_nodes_from(item)
        parent_0 = result.get(item[0])
        node_list_0 = [parent_0]
        parent_1 = result.get(item[1])
        node_list_1 = [parent_1]
        weight = 1
        while parent_0 != None or parent_1 != None:
            if parent_0 != None:             
                parent_0 = result.get(parent_0)
                node_list_0.append(parent_0)
            if parent_1 != None:             
                parent_1 = result.get(parent_1)
                node_list_1.append(parent_1)            
        node_list_0.reverse()        
        node_list_1.reverse()       
        for (node1,node2) in zip(node_list_0, node_list_1):
            if node1 != node2:
                break
            weight = float(weight + 1)
        G.add_weighted_edges_from([(item[0],item[1],weight)])   
    return G    

def addtoGraph(activity_pair, G):
    for item in activity_pair:
        tuple(item)
        if G.has_edge(*item):
            weight = G[item[0]][item[1]]['weight']
            weight = float(weight + .01)
            print weight
            G[item[0]][item[1]]['weight']= weight


    
if __name__ == "__main__":
    result = getCateTree()
    G = getinitGraph(result)
    