import tweepy
import configparser

def load_config(version):
    configs = configparser.ConfigParser()
    configs.read('config.ini')
    keys = configs['TWITTER']
    consumer_key = keys['TWITTER_C_KEY'] 
    consumer_secret = keys['TWITTER_C_SECRET'] 
    access_token = keys['TWITTER_A_KEY']
    access_secret = keys['TWITTER_A_SECRET']
    bearer_token = keys['BEARER_TOKEN']
    if version == "v1":
        return consumer_key, consumer_secret, access_token, access_secret
    elif version == "v2":
        return bearer_token

def connect_to_twitter_api():
    consumer_key, consumer_secret, access_token, access_secret= load_config("v1")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

def connect_to_twitter_api_v2():
    bearer_token = load_config("v2")
    return tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

api = connect_to_twitter_api()
client = connect_to_twitter_api_v2()
