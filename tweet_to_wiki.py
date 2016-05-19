# -*- coding: utf-8 -*-
"""
Created on Wed May 18 21:33:52 2016

@author: Akshta
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 04 06:39:34 2016

@author: Akshta
"""
Map = {}
for line in open('twitter_wiki_map.txt'):
    listWords = line.split("\t")
    Map[listWords[0]] = listWords[1][:-1]

f = open('pair_data/val/val_mod.txt', 'w')

for line in open('pair_data/val/val_pure.txt'):
    listWords = line.split(",")
    string = ''
    for word in listWords:
        if word[-1] == '\n':
            string = string + Map[word[:-1]] + ','
        else:
            string = string + Map[word] + ','
    string = string[:-1]
    f.write(string + '\n')
    
f.close()