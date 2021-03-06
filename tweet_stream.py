#Miguel Aroca-Ouellette
#Modified from: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
#Bounding box: http://stackoverflow.com/questions/22889122/how-to-add-a-location-filter-to-tweepy-module

#Import the necessary methods from tweepy library
import tweepy
import json
import sys
#Variables that contains the user credentials to access Twitter API

#for string matching
import time

cred_file='credentials.txt'
act_file='activity_list.txt'
user_file='user_set.txt'

def main():
    myTweetReader=TweetReader(cred_file,act_file,'rest',10)
    #myTweetReader.start_stream('activity')
    myTweetReader.search_rest()

class StdOutListener(tweepy.StreamListener):
    """Basic listener which prints username and Tweets"""

    def __init__(self,num_prev,user_max):
        self.client=None
        self.num_prev=num_prev
        self.user_max=user_max
        self.user_count=0

        #open output file
        self.out=None
        self.first=False
        self.user_set=load_users()

    def set_output(self,output_file):
        #close file if necessary
        try:
            self.out.close()
        except AttributeError:
            pass
        #set new output file
        self.out=open(output_file,'a')
        self.user_set=set()

    def on_data(self, data):
        """Handles succesful data fetch"""

        if not self.out:
            #wait for output file to be set
            return True

        tweet_dict=self.parse_tweet(data)

        if tweet_dict['user'] in self.user_set:
            return True

        self.write_out(tweet_dict) #only write out some of the data

        #print "--------------------------------"
        #print "\t\t\tUser: "+tweet_dict['user']+" tweeted: "
        #print "\t"+tweet_dict['text']
        self.get_last_tweet(tweet_dict['user'])

        #prevents current user from getting mined twice in this session
        # or in next sessions
        self.user_set.add(tweet_dict['user'])
        self.write_user(tweet_dict['user'])
        self.user_count+=1

        print str(self.user_count)+": "+str(tweet_dict['user'])

        if (self.user_max) and (self.user_count>=self.user_max):
            #finished with this file
            self.out.close()
            self.out=None
            self.user_count=0
            sys.exit(0)

        return True

    def on_error(self, status):
        print status

    def set_client(self,client):
        self.client=client

    def get_last_tweet(self,username):
        new_tweets = self.client.user_timeline(screen_name=str(username),count=self.num_prev)
        count=0
        for tweet in new_tweets[1:]:
            #skip first tweet
            tweet_dict=dict(self.parse_tweet(json.dumps(tweet._json)))
            self.write_out(tweet_dict)
            #print str(count)+":\t"+text
            #self.check_for_activity(text)
            count+=1
        return count

    def parse_tweet(self,tweet):
        """Returns dictionary from tweet json"""
        tweet_dict={}
        if (type(tweet) is str) or (type(tweet) is unicode):
            tweet_json=json.loads(tweet)
            tweet_dict['user']=tweet_json['user']['screen_name'].encode('ascii','ignore')
            tweet_dict['text']=tweet_json['text'].encode('ascii','ignore')
            try:
                tweet_dict['location']=tweet_json['user']['location'].encode('ascii','ignore')
            except AttributeError:
                tweet_dict['location']=""
            tweet_dict['time']=tweet_json['created_at'].encode('ascii','ignore')
        else:
            #tweepy.models.Status type
            try:
                #ignores special unicode characters
                tweet_dict['user']=tweet.author.screen_name.encode('ascii','ignore')
                tweet_dict['text']=tweet.text.encode('ascii','ignore')
                tweet_dict['location']=tweet.user.location.encode('ascii','ignore')
                tweet_dict['time']=tweet.created_at.encode('ascii','ignore')
            except UnicodeEncodeError:
                pass

        return tweet_dict

    def write_out(self,tweet):
        """Writes tweet out to file"""
        json.dump(tweet,self.out)
        self.out.write("\n") #one json per line

    def write_user(self,user):
        """Adds user to user file. This avoids loading him in the future"""
        with open(user_file,'a') as f:
            f.write(user+'\n')

        f.close()

#Stream class
class TweetReader():

    def __init__(self,cred_file,activity_file,mode,user_max=None):

        #filters
        self.NA_bounding_box=[-139.7,25.5,-44.1,59.9]

        #variables
        num_prev=200 #rate limit

        #initialization
        self.mode=mode
        self.access_token=""
        self.access_token_secret=""
        self.consumer_key=""
        self.consumer_secret=""
        self.stream=None
        self.activity_list=[]
        load_activities(activity_file,self.activity_list)
        self.fetch_credentials(cred_file)
        self.client=None
        self.handler = StdOutListener(num_prev,user_max)
        self.init()
        if self.mode not in ['stream','rest']:
            print "Invalid mode!"
            raise (AssertionError)

    def init(self):
        """This handles Twitter authetification and the connection to Twitter Streaming API"""

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.client = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
        self.handler.set_client(self.client)
        if self.mode=='stream':
            self.stream = tweepy.Stream(auth, self.handler)

    def fetch_credentials(self,filename):
        """Read from credential file"""

        with open(filename,'r') as f:
            self.access_token=f.readline().rstrip()
            self.access_token_secret=f.readline().rstrip()
            self.consumer_key=f.readline().rstrip()
            self.consumer_secret=f.readline().rstrip()

        f.close()

    def search_rest(self):
        """Uses the REST API to search for activities"""
        if self.mode!='rest':
            print "Invalid mode!"
            return

        goal_users=200
        max_tweets=100
        user_set=load_users()

        for activity in self.activity_list:
            print "Gathering data for "+activity
            self.handler.set_output("tweet_by_activity/output_"+activity+".txt")
            user_count=0
            max_id=None
            while True:
                try:
                    if not max_id:
                        #get all new tweets
                        results = self.client.search(activity,lang='en',count=max_tweets)
                    else:
                        #get subsequent tweets (older than max id, i.e. smaller)
                        results = self.client.search(activity,lang='en',count=max_tweets,max_id=str(max_id-1))
                    for tweet in results:
                        tweet_dict=self.handler.parse_tweet(json.dumps(tweet._json))
                        user=tweet_dict['user']
                        max_id=tweet.id
                        if user not in user_set: #TO DO: FIx and reset
                            self.handler.write_out(tweet_dict)
                            count=self.handler.get_last_tweet(user)
                            self.handler.write_user(user)
                            user_set.add(user)
                            print str(user_count)+": "+tweet_dict['user']+" "+str(count)
                            user_count+=1
                        if user_count==goal_users:
                            break
                    if user_count==goal_users:
                        break
                except tweepy.TweepError, e:
                    print e

    def start_stream(self,type_filter):
        """Starts stream and filters on either activity or location"""
        if self.mode!='stream':
            print "Invalid mode!"
            return
        for activity in self.activity_list:
            done=False
            while True:
                print "Gathering data for "+activity
                try:
                    self.handler.set_output("tweet_by_activity/output_"+activity+".txt")
                    if type_filter=="activity":
                        self.stream.filter(track=[activity])
                    elif type_filter=="location":
                        self.stream.filter(locations=self.NA_bounding_box)
                    else:
                        print "start_stream error(): invalid input!"
                        raise (AssertionError)
                except:
                    if type(sys.exc_info()[1])==SystemExit and sys.exc_info()[1].code==0:
                        print "Finished gathering tweets for "+activity
                        self.stream.disconnect()
                        done=True
                    else:
                        print "Unexpected error: "+str(sys.exc_info()[0])+str(sys.exc_info()[1])

                if done:
                    break

def load_users():
    with open(user_file,'r') as f:
        users=set(f.readlines())

    f.close()

    return users

def load_activities(filename,activity_list):
    with open(filename,'r') as f:
        for line in f:
            if len(line.split("/"))>1:
                activity_list+=(line.lower().rstrip().split("/"))
            else:
                activity_list.append(line.lower().rstrip())

    f.close()

def fix_activity_list():
    f1=open('activity_list.txt','r')
    f2=open('new.txt','w')

    for line in f1:
        if (line[0] in ['4','5']) or len(line)<=1 or ("Suggested" in line):
            continue
        f2.writelines(line)

    f1.close()
    f2.close()

if __name__ == '__main__':
    main()