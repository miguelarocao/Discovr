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



ip = sys.argv[1:]
if len(ip) == 0:
    ip = ['Archery ','Baseball','Softball',]

for elem in ip:
    id = activs.index(elem)
    del activs[id]
    
scores = dict()
for elem in activs:
    scores[elem] = 0

for key in ip:
    for elem in activs:
        scores[elem] += weights[key][elem]
    
factor = sum(scores.itervalues())    
for key in scores:
    scores[key] /= factor

for activity in ip:
    scores.pop(activity, None)

print sorted(scores, key=scores.get, reverse=True)[:5]


