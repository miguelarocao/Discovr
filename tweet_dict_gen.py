# -*- coding: utf-8 -*-
"""
Created on Wed May 04 06:39:34 2016

@author: Akshta
"""
Map = {}
for line in open('twitter_wiki_map.txt'):
    listWords = line.split("\t")
    Map[listWords[0]] = listWords[1][:-1]


dict_final = {}
dict_activity = {}
    
for line in open('pair_data\output_pairs20160510-234931.txt'):
    listWords = line.split(",")
    score = float(listWords[2])
    activity_1 = Map[listWords[0]]
    activity_2 = Map[listWords[1]]
    if activity_1 != activity_2:
        if not dict_final.has_key(activity_1):    
            dict_final[activity_1] = {}
        if not dict_final[activity_1].has_key(activity_2):        
            dict_final[activity_1][activity_2] = score   
        else:
            dict_final[activity_1][activity_2] = dict_final[activity_1][activity_2] + score           


for key in dict_final.keys():
    sum_dict = sum(dict_final[key].values())
    if sum_dict == 0:
        dict_final[key].update((x, 0) for x, y in dict_final[key].items())
        print key
    else:    
        dict_final[key].update((x, y/sum_dict) for x, y in dict_final[key].items())            
    
import json
with open('result_tweet.json', 'w') as fp:
    json.dump(dict_final, fp)    
    




