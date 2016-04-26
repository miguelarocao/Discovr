#TODO: Get 100 users PER activity (20000 tweets)
#TODO: Store tweets as json (same info, just easier to work with)

from tweet_stream import load_activities
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time


#confidence of matchign with a word
FUZZ_CONFIDENCE=85

#globals
activity_list=[]

#output pairs file
timestr=time.strftime("%Y%m%d-%H%M%S")
out_pair="pair_data/output_pairs"+timestr+".txt"
out_user="pair_data/user_pairs"+timestr+".txt"

def main():
    weekdays=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    load_activities('activity_list.txt',activity_list)
    act_dict=build_dict()

    userfile=open(out_user,'a')

    filenames=['output_tweets.txt','output_tweets2.txt']
    tweet_count=0
    user_count=0
    curr_user=''
    in_tweet=0
    user_tweets=[]
    to_print=False
    start_time=time.clock()
    for filename in filenames:
        with open(filename,'r') as f:
            while True:
                line=f.readline()
                if line=="":
                    #file done!
                    break

                #file not done
                line=line.rstrip()

                if (line[0:3] in weekdays) and (line[4:7] in months) and len(line)==30:
                    #new tweet
                    tweet_count+=1
                    in_tweet=0
                elif in_tweet==2:
                    #checks username
                    if curr_user!=line:
                        #new user
                        if user_count>0:
                            user_pop_dict(userfile,curr_user,act_dict,user_tweets)
                            user_tweets=[] #reset user tweets
                        user_count+=1
                        curr_user=line
                        print str(user_count)+": "+curr_user
                        #return
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
    print "Time: "+str(time.clock()-start_time)

    f.close()
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
        for j in range(i,len(activity_list)):
            act_dict[tuple(sorted([activity_list[i],activity_list[j]]))]=0

    return act_dict

def user_pop_dict(userfile,user,act_dict,tweets):
    """Populates dictionary based on tweets from a single user"""


    userfile.write(user+'\n')

    user_act=set()
    count=0
    for tweet in tweets:
        user_act.update(check_for_activity(tweet))
        count+=1

    user_act=list(user_act)
    userfile.write(",".join(user_act)+'\n')
    for i in range(len(user_act)):
        for j in range(i,len(user_act)):
            act_dict[tuple(sorted([user_act[i],user_act[j]]))]+=1

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
    reparse_user_pairs("pair_data/user_pairs20160425-101756.txt")
    #main()
