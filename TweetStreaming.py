import tweepy
from tweepy import OAuthHandler, Stream

from tweepy.streaming import StreamListener
import socket
import json

consumer_key = 'consumer key'
consumer_secret = 'consumer secret'
access_token = 'access_token'
access_secret = 'access_secret'

tweet_count = 0
num_of_tweets = 1500
savefile = open('tweet.txt', 'w+')
class TweetListener(StreamListener):
    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            global savefile
            global tweet_count
            global num_of_tweets
            
            msg = json.loads(data)
            hashtag = msg['entities']['hashtags']
            tag = ''
            
            if tweet_count < num_of_tweets:
                print(msg['text'].encode('utf-8'))
                self.client_socket.send((str(msg['text'])+"\n").encode('utf-8'))
                savefile.write(msg['created_at'] + '\t' +str(msg['text'].encode('utf-8'))  + '\n')
                tweet_count +=1
            return True
            
            # return True
        except BaseException as e:
            print("ERROR ", e)
        return True

    def on_error(self, status):
        print(status)
        return True

savefile.close()

def sendData(c_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetListener(c_socket))
    twitter_stream.filter(track=['Taxi', 'taxi'], locations=[-79.762152,40.496103, -71.856214,45.01585], languages=['en'])


if __name__ == "__main__":
    s = socket.socket()         # Create a socket object
    host = "127.0.0.1"     # Get local machine name
    port = 5553                 # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port

    print("Listening on port: %s" % str(port))

    s.listen(5)                 # Now wait for client connection.
    c, addr = s.accept()        # Establish connection with client.

    print("Received request from: " + str(addr))

    sendData(c)
