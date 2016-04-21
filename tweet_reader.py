#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Miguel
#
# Created:     17/04/2016
# Copyright:   (c) Miguel 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from tweet_stream import load_activities

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#confidence of matchign with a word
FUZZ_CONFIDENCE=85

#globals
activity_list=[]

#output pairs file
out_pair="output_pairs.txt"

def main():
    weekdays=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

    load_activities('mod_activity_list.txt',activity_list)
    act_dict=build_dict()

    filename='output.txt'
    tweet_count=0
    user_count=0
    curr_user=''
    in_tweet=0
    user_tweets=[]
    with open(filename,'r') as f:
        while True:
            line=f.readline().rstrip()

            if line[0:3] in weekdays:
                #new tweet
                tweet_count+=1
                in_tweet=0
                if tweet_count%50000==0:
                    print tweet_count
            elif in_tweet==2:
                #checks username
                if curr_user!=line:
                    #new user
                    if user_count>0:
                        user_pop_dict(act_dict,user_tweets)
                        user_tweets=[] #reset user tweets
                    user_count+=1
                    curr_user=line
                    print "user: "+curr_user
                    if user_count>5:
                        break
            elif in_tweet==1:
                #location
                pass
            else:
                #tweet!
                user_tweets.append(line)

            in_tweet+=1

    for key,value in act_dict.iteritems():
        if value>0:
            print str(key)+": "+str(value)

    write_out_pairs(act_dict)

    print "Num tweets: "+str(tweet_count)
    print "Num users: "+str(user_count)

    f.close()

def write_out_pairs(act_dict):
    """Writes pairs out to output file."""
    with open(out_pair,'w') as f_pair:
        for key,value in act_dict.iteritems():
            f_pair.write(" ".join([key[0],key[1],str(value)])+"\n")

    f_pair.close()

def build_dict():
    """Returns dictionary corresponding to paired activities.
    Pairs are sorted alphabetically. i.e. (Basketball, Volleyball)"""

    act_dict={}

    for i in range(len(activity_list)):
        for j in range(i+1,len(activity_list)):
            act_dict[tuple(sorted([activity_list[i],activity_list[j]]))]=0

    return act_dict

def user_pop_dict(act_dict,tweets):
    """Populates dictionary based on tweets from a single user"""

    user_act=set()
    count=0
    for tweet in tweets:
        user_act.update(check_for_activity(tweet))
        count+=1

    user_act=list(user_act)
    for i in range(len(user_act)):
        for j in range(i+1,len(user_act)):
            act_dict[tuple(sorted([user_act[i],user_act[j]]))]+=1
    return

def check_for_activity(tweet):
    """Checks tweet to see if it contains activities. Returns set of matched activities."""
    match_activities=set()
    match_val=[]
    tweet=tweet.lower()
    tweet_words=tweet.split(" ")
    for activity in activity_list:
        if len(activity.split(" "))>1:
            #multiword match
            match=fuzz.partial_ratio(activity,tweet)
            if match>FUZZ_CONFIDENCE:
                match_activities.add(activity)
        else:
            for word in tweet_words:
                #single word match
                match=fuzz.ratio(activity,word)
                if match>FUZZ_CONFIDENCE:
                    match_activities.add(activity)
                    break

    return match_activities

if __name__ == '__main__':
    main()
