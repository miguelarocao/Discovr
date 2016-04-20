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
FUZZ_CONFIDENCE=95

#globals
activity_list=[]

def main():
    weekdays=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

    act_dict=load_activities('activity_list.txt',activity_list)

    filename='output.txt'
    tweet_count=0
    user_count=0
    curr_user=''
    in_tweet=0
    user_tweets=[]
    with open(filename,'r') as f:
        while True:
            line=f.readline().rstrip()
            if line=="":
                #skip blank lines
                continue
            elif line[0:3] in weekdays:
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
                        break
                    user_count+=1
                    curr_user=line
                    print curr_user

            elif in_tweet==1:
                #location
                pass
            else:
                #tweet!
                user_tweets.append(line)

            in_tweet+=1

            if tweet_count>200:
                break

    print "Num tweets: "+str(tweet_count)
    print "Num users: "+str(user_count)

    f.close()

def build_dict(activities):
    """Returns dictionary matrix corresponding to paired activities"""

    act_dict={}
    base_dict=dict((key,0) for key in act_dict)

    for activity in activities:
        act_dict[activity]=dict(base_dict)

    return act_dict

def user_pop_dict(act_dict,tweets):
    """Populates dictionary based on tweets from a single user"""

    user_act=[]
    count=0
    for tweet in tweets:
        user_act+=check_for_activity(tweet)
        print count
        count+=1

    print user_act
    return

def check_for_activity(tweet):
    """Checks tweet to see if it contains activities."""
    match_activities=[]
    match_val=[]
    for activity in activity_list:
        for word in tweet.split(" "):
            match=fuzz.ratio(activity.lower(),word.lower())
            if match>FUZZ_CONFIDENCE:
                match_activities.append(activity)
                match_val.append(match)

    return match_activities

if __name__ == '__main__':
    main()
