# -*- coding: utf-8 -*-
import json
import sys

with open('weights.json', 'r') as fp:
   weights = json.load(fp)

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




Map = {}
Reverse_Map = {}
for line in open('wiki_to_gmap.txt'):
    listWords = line.split("\t")
    Map[listWords[1][:-1]] = listWords[0]
    Reverse_Map[listWords[0]] = listWords[1][:-1]


ip = sys.argv[1:]

ip = list(set(ip))
if len(ip) == 0:
    ip = ['Baseball','Softball']

# convert to wiki keys
for elem in ip:
    if elem in Map:
        id = ip.index(elem)
        ip[id] = Map[elem]

for elem in ip:
    if elem in activs:
        id = activs.index(elem)
        del activs[id]
        
scores = dict()

for elem in activs:
    scores[elem] = 0

for key in ip:
    for elem in activs:
        if key in weights:
            scores[elem] += weights[key][elem]
    
factor = sum(scores.itervalues())    
for key in scores:
    scores[key] /= factor

for activity in ip:
    scores.pop(activity, None)

toprint = sorted(scores, key=scores.get, reverse=True)[:5]

new_toprint = [Reverse_Map[x] for x in toprint]
print new_toprint

