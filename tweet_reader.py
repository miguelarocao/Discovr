from tweet_stream import load_activities
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
import json
import sys

#confidence of matchign with a word
FUZZ_CONFIDENCE=85

MAX_TWEET=200

#globals
activity_list=[]

#output pairs file
timestr=time.strftime("%Y%m%d-%H%M%S")
out_pair="pair_data/output_pairs"+timestr+".txt"
out_user="pair_data/user_pairs"+timestr+".txt"

def main():
    load_activities('activity_list.txt',activity_list)
    act_dict=build_dict()

    userfile=open(out_user,'a')

    tweet_count=0
    user_count=0
    user_count=0
    start_time=time.clock()
    curr_user=None
    user_tweets=[]
    for activity in activity_list:
        filename="tweet_by_activity/output_"+activity+".txt"
        with open(filename,'r') as f:
            tweet_list=json.load(f)
            curr_user=tweet_list[0]["user"]
            user_list=[]
            for tweet in tweet_list:
                if (str(tweet['user'])!=curr_user or
                    len(user_tweets)>MAX_TWEET or tweet_count==len(tweet_list)-1):
                    user_pop_dict(activity,userfile,curr_user,act_dict,user_tweets)
                    print str(user_count)+" ("+activity+"): "+curr_user
                    user_count+=1
                    user_tweets=[]
                    curr_user=tweet['user']

                user_tweets.append(tweet["text"])
                tweet_count+=1

        f.close()

    write_out_pairs(act_dict)

    print "Num tweets: "+str(tweet_count)
    print "Num users: "+str(user_count)
    print "Time: "+str(time.clock()-start_time)


    userfile.close()

def reparse_user_pairs(filename):
    """Reparses user activity pairs."""

    load_activities('activity_list.txt',activity_list)
    act_dict=build_dict()

    read_line=False

    with open(filename,'r') as f:
        lines=f.readlines()
        for line in lines:
            line=line.rstrip()
            if line=="":
                read_line=False
                continue
            if read_line:
                #activtiies
                activities=line.split(",")
                for i in range(len(activities)):
                    for j in range(i,len(activities)):
                        act_dict[tuple(sorted([activities[i],activities[j]]))]+=1

            read_line=True

    f.close()
    write_out_pairs(act_dict)


def write_out_pairs(act_dict):
    """Writes pairs out to output file."""
    with open(out_pair,'w') as f_pair:
        for key,value in act_dict.iteritems():
            f_pair.write(",".join([key[0],key[1],str(value)])+"\n")

    f_pair.close()


def build_dict():
    """Returns dictionary corresponding to paired activities.
    Pairs are sorted alphabetically. i.e. (Basketball, Volleyball)"""

    act_dict={}

    for i in range(len(activity_list)):
        for j in range(len(activity_list)):
            act_dict[tuple([activity_list[i],activity_list[j]])]=0

    return act_dict

def user_pop_dict(primary,userfile,user,act_dict,tweets):
    """Populates dictionary based on tweets from a single user.
    Also writes out user pairs."""

    userfile.write(user+'\n')
    userfile.write(primary+'\n')

    user_act=set([primary])
    count=0
    for tweet in tweets:
        user_act.update(check_for_activity(tweet))
        count+=1

    user_act=list(user_act)
    userfile.write(",".join(user_act)+'\n')
    for i in range(len(user_act)):
        for j in range(len(user_act)):
            act_dict[tuple([user_act[i],user_act[j]])]+=1

    userfile.write('\n')
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
    #reparse_user_pairs("pair_data/user_pairs20160425-101756.txt")
    main()
