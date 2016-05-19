# -*- coding: utf-8 -*-
import json
import sys
import copy

with open('weights.json', 'r') as fp:
   weights = json.load(fp)

#fail = open('failures.txt', 'w')

activs = [
'Bowling',
'Dance',
'Disc Golf',
'Go Kart',
'Laser Tag',
'Mini Golf',
'Golf',
'Swimming (sport)',
'Salsa (dance)',
'Samba',
'Baseball',
'Basketball',
'Cricket',
'American football',
'Hockey',
'Racquetball',
'Association football',
'Table Tennis',
'Tennis',
'Track and field',
'Running',
'Badminton',
'Curling',
'Boxing',
'Physical fitness',
'Sport Climbing',
'Rock Climbing',
'Cycling',
'Gymnastics',
'Martial Arts',
'Yoga',
'Paddleboarding',
'Field Hockey',
'Paintball',
'Rugby football',
'Skateboarding',
'Inline skating',
'Roller skating',
'Squash (sport)',
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
'Pool (cue sports)',
'Paragliding',
'Handball',
'Pottery',
'Photography',
'Painting',
'Drawing',
'Singing',
'Improvisational theatre',
'Comedy',
'Theatre',
'Origami',
'Sculpture',
'Karaoke',
'Charity shop',
'Reading (process)',
'Escape room',
'Gambling ',
'Arcade game',
]

fail_count = dict()
for act in activs:
    fail_count[act] = [0, 0]

def recommend(ip):
    # remove duplicate inputs
    ip_set = set(ip)
    ip = list(ip_set)
    acts = copy.deepcopy(activs)
    for elem in ip:
        if elem in acts:
            id = acts.index(elem)
            del acts[id]
            
    scores = dict()
    
    for elem in acts:
        scores[elem] = 0
    
    for key in ip:
        for elem in acts:
            if key in weights:
                scores[elem] += weights[key][elem]
            else:
                raise ValueError('Input not in list of activities')

    #factor = sum(scores.itervalues())
    #for key in scores:
    #    scores[key] /= factor
    
    #for activity in ip:
    #    scores.pop(activity, None)
    
    return sorted(scores, key=scores.get, reverse=True)
    
def validate(ip):
    # remove duplicate inputs
    ip_set = set(ip)
    ip = list(ip_set)
    sum_rank = 0
    count = 0
    pred = 0
    for i in range(len(ip)):
        act_list = copy.deepcopy(ip)
        del act_list[i]
        res = recommend(act_list)
        rank = res.index(ip[i])
        fail_count[ip[i]][0] += 1
        if rank < 5:
            pred += 1
        else:
            fail_count[ip[i]][1] += 1
            #fail.write(ip[i] + "\n")
            #print ip[i]
        sum_rank += rank
        count += 1
        
    return [sum_rank, pred, count]

with open('pair_data/val/val_subsample_mod.txt') as f:
    count = 0
    sum_pred = 0
    sum_rank = 0
    norm_sum_pred = 0
    norm_count = 0
    for line in f:
        line = line[0:-1]
        ip = line.split(",")
        [sum_r, pred, cnt] = validate(ip)
        sum_rank += sum_r
        sum_pred += pred
        count += cnt
        norm_sum_pred += float(pred)/cnt
        norm_count += 1
    avg_rank = float(sum_rank)/count
    avg_pred = float(sum_pred)/count
    avg_norm_pred = float(norm_sum_pred)/norm_count

#fail.close()