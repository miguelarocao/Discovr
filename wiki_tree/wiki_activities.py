# -*- coding: utf-8 -*-

import networkx as nx
import pickle
from wikitools import wiki
from wikitools import page
# from wikitools import category

# Load the graph
with open('objs.pickle') as f:
    G, lst, level, id = pickle.load(f)
# Reverse graph to get faster results
G_rev = G.reverse()



class Wiki_Activities:

    def __init__(self, acts):
        self.acts = acts
        self.site = wiki.Wiki("http://en.wikipedia.org/w/api.php")        
        self.root = 'Main topic classifications'
        self.score_exponent = 1.1
        self.G = G
        self.G_rev = G_rev
        
        act_data = dict()
        for act in acts:
            act_data[act] = self.get_paths(act)
            
        # Get activity data
        self.act_data = act_data
        
        # Get category counts
        self.node_counts = self.gen_node_counts()

    # Get the parent categories and related information for
    # an activity
    def get_paths(self, act):
        pg = page.Page(self.site, act)
        cat = pg.getCategories()
        
        cat_ = []
        path_ = []
        set_ = []
        for c in cat:
            c = c[9:]
            if c in self.G:
                cat_.append(c)
                p = nx.dijkstra_path(self.G_rev, c, self.root)
                path_.append(p)
                s = set(p)
                set_.append(s)
            
        return [cat_, path_, set_]    
    
    # Generate the node counts to determine how common
    # a category is over the set of all activities
    def gen_node_counts(self):
        cats = dict()
        for elem in self.acts:
            [cat1, path1, set1] = self.act_data[elem]
            for p in path1:
                for e in p:
                    if e in cats:
                        cats[e] += 1
                    else:
                        cats[e] = 1
        return cats
    
    def score_depth(depth):
        return depth
    
    def score_node_counts(self, node, depth):
        return self.score_exponent**(-self.node_counts[node])
        
    # Get the best common path between two parent categories
    def find_best_common_category(self, act_data, act_data2):
        [cat_, path_, set_] = act_data
        [cat2_, path2_, set2_] = act_data2
        curr_max = 0
        curr_pair = [0, 0]
        curr_depth = 0
        curr_node = ''
        if len(set_) * len(set2_) == 0:
            raise Exception('Empty input')
        for i in range(len(set_)):
            for j in range(len(set2_)):
                common = set_[i].intersection(set2_[j])
                #print common
                depth = len(common)
                #print depth
                node = path_[i][-depth]
                scor = self.score_node_counts(node, depth)
                if(scor > curr_max):
                    curr_max = scor
                    curr_pair = [i, j]
                    curr_depth = depth
                    curr_node = node
        
        print 'Paired "' + cat_[curr_pair[0]] + '" with "' + cat2_[curr_pair[1]] + '" node = "' + \
            curr_node + '" at depth = ' + str(curr_depth)
        return [curr_max, curr_pair[0], curr_pair[1]]
    
    # Get the best common path between two activities
    def find_best_common_path(self, act, act2):
        [score, p1, p2] = self.find_best_common_category(self.act_data[act], self.act_data[act2])        
        return [score, self.act_data[act][1][p1], self.act_data[act2][1][p2]]
        
    def find_score(self, act, act2):
        [cat_, path_, set_] = self.act_data[act]
        [cat2_, path2_, set2_] = self.act_data[act2]
        
        m = len(cat_)
        n = len(cat2_)        
        k = min(m, n)
        score = 0
        
        while k > 0:
            act_data = [cat_, path_, set_]
            act_data2 = [cat2_, path2_, set2_]
            [sc, p1, p2] = self.find_best_common_category(act_data, act_data2)
            score += sc
            del cat_[p1]
            del path_[p1]
            del set_[p1]
            del cat2_[p2]
            del path2_[p2]
            del set2_[p2]
            k -= 1
        return score

# def main():
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

act_pair = [
'Bowling',
'Curling',
]

wiki_obj = Wiki_Activities(acts)
node_counts = wiki_obj.node_counts

[cat1, path1, set1] = wiki_obj.get_paths(act_pair[0])
[cat2, path2, set2] = wiki_obj.get_paths(act_pair[1])

# [scor, p, p2] = wiki_obj.find_best_common_path(act_pair[0], act_pair[1])
score = wiki_obj.find_score(act_pair[0], act_pair[1])

#if __name__ == '__main__':
#    main()