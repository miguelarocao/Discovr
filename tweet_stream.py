#Miguel Aroca-Ouellette
#Modified from: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
#Bounding box: http://stackoverflow.com/questions/22889122/how-to-add-a-location-filter-to-tweepy-module

#Import the necessary methods from tweepy library
import tweepy
import json
import sys
#Variables that contains the user credentials to access Twitter API

#for string matching
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def main():
    myTweetStream=TweetStream('credentials.txt','activity_list.txt','output.txt',50000)
    myTweetStream.start_stream('activity')

class StdOutListener(tweepy.StreamListener):
    """Basic listener which prints username and Tweets"""

    def __init__(self,num_prev,activity_list,output_file,tweet_max):
        self.client=None
        self.num_prev=num_prev
        self.tweet_max=tweet_max
        self.tweet_count=0
        self.activity_list=activity_list

        #variables
        self.fuzz_confidence=95

        #open output file
        self.out=open(output_file,'w')

    def on_data(self, data):
        """Handles succesful data fetch"""
        #print data

        user,text,loc,time=self.parse_tweet(data)
        self.write_out([time,loc,user,text])

        print "--------------------------------"
        print "\t\t\tUser: "+str(user)+" tweeted: "
        print "\t"+text
        count=self.get_last_tweet(user)

        self.tweet_count+=count
        if (self.tweet_max) and (self.tweet_count>=self.tweet_max):
            self.close_listener()
            sys.exit(0)

        print self.tweet_count
        return True

    def on_error(self, status):
        print status

    def set_client(self,client):
        self.client=client

    def get_last_tweet(self,username):
        new_tweets = self.client.user_timeline(screen_name=str(username),count=self.num_prev)
        count=0
        for tweet in new_tweets:
            if count==0:
                #skip first tweet
                count+=1
                continue
            user,text,loc,time=self.parse_tweet(json.dumps(tweet._json))
            self.write_out([time,loc,user,text])
            #print str(count)+":\t"+text
            #self.check_for_activity(text)
            count+=1
        return count

    def parse_tweet(self,tweet):
        """Returns username,text,location,time from tweet"""
        if (type(tweet) is str) or (type(tweet) is unicode):
            tweet_json=json.loads(tweet)
            user=tweet_json['user']['screen_name'].encode('ascii','ignore')
            text=tweet_json['text'].encode('ascii','ignore')
            try:
                loc=tweet_json['user']['location'].encode('ascii','ignore')
            except AttributeError:
                loc=""
            time=tweet_json['created_at'].encode('ascii','ignore')
        else:
            #tweepy.models.Status type
            try:
                #ignores special unicode characters
                user=tweet.author.screen_name.encode('ascii','ignore')
                text=tweet.text.encode('ascii','ignore')
                loc=tweet.user.location.encode('ascii','ignore')
                time=tweet.created_at.encode('ascii','ignore')
            except UnicodeEncodeError:
                pass

        return user,text,loc,time

    def check_for_activity(self,tweet):
        """Checks tweet to see if it contains activity. Looks for best match."""
        best_match=self.fuzz_confidence
        best_activity=None
        best_word=None
        for activity in self.activity_list:
            for word in tweet.split(" "):
                match=fuzz.ratio(activity.lower(),word.lower())
                if match>best_match:
                    best_match=match
                    best_activity=activity
                    best_word=word

        if best_activity:
            #print best_match
            #print best_activity
            #print best_word
            return True
        return False

    def write_out(self,tweet):
        """Writes tweet out to file"""
        self.out.write("\n".join(tweet)+"\n\n")

    def close_listener(self):
        """Closes listener and output file"""
        self.out.close()


#Stream class
class TweetStream():

    def __init__(self,cred_file,activity_file,output_file,tweet_max=None):
        #filters
        self.NA_bounding_box=[-139.7,25.5,-44.1,59.9]
        self.activity_filter=['basketball','yoga','baseball']

        #variables
        num_prev=1

        #initialization
        self.access_token=""
        self.access_token_secret=""
        self.consumer_key=""
        self.consumer_secret=""
        self.stream=None
        self.activity_list=[]
        self.load_activities(activity_file)
        self.listen = StdOutListener(num_prev,self.activity_list,output_file,tweet_max)
        self.fetch_credentials(cred_file)
        self.setup_credentials()

    def setup_credentials(self):
        """This handles Twitter authetification and the connection to Twitter Streaming API"""


        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        client = tweepy.API(auth)
        self.listen.set_client(client)
        self.stream = tweepy.Stream(auth, self.listen)

    def fetch_credentials(self,filename):
        """Read from credential file"""

        with open(filename,'r') as f:
            self.access_token=f.readline().rstrip()
            self.access_token_secret=f.readline().rstrip()
            self.consumer_key=f.readline().rstrip()
            self.consumer_secret=f.readline().rstrip()

        f.close()

    def start_stream(self,mode):
        """Starts stream and filters on either activity or location"""
        if mode=="activity":
            self.stream.filter(track=self.activity_filter)
        elif mode=="location":
            self.stream.filter(locations=self.NA_bounding_box)
        else:
            print "start_stream error(): invalid input!"
            raise

    def load_activities(self,filename):
        with open(filename,'r') as f:
            for line in f:
                self.activity_list.append(line.rstrip())
                if len(line.split(" "))>1:
                    self.activity_list.append(" ".join(line.rstrip().split(" ")[:-1])) #also remove last word

        f.close()

def parse_json(fields):
    """Groups tweets by users. Input specifies desired fields returned.
    Input: list of json fields returned.
    Output: list of list of [users[tweet fields]]"""

    pass

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