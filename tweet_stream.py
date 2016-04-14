#Miguel Aroca-Ouellette
#Modified from: http://adilmoujahid.com/posts/2014/07/twitter-analytics/

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

#TO DO: Read Keys to/from file so I can put this on GitHub

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

def fetch_credentials(filename):
    """Read from credential file"""
    global access_token, access_token_secret, consumer_key, consumer_secret

    with open(filename,'r') as f:
        access_token=f.readline().rstrip()
        access_token_secret=f.readline().rstrip()
        consumer_key=f.readline().rstrip()
        consumer_secret=f.readline().rstrip()

    f.close()

def stream():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])

if __name__ == '__main__':
    fetch_credentials('credentials.txt')
    stream()