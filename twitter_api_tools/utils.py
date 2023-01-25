from twitter_api_tools import api, client
import tweepy
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import pytz
import logging

UTC = pytz.UTC

def get_user_single(screen_name=None, user_id=None):
    try:
        if screen_name:
            user_json = api.get_user(screen_name = screen_name)
        elif user_id:
            user_json = api.get_user(user_id=user_id)
        return user_json
    except tweepy.NotFound:
        pass

class User_list:
    def __init__(self, screen_name_list=None, user_id_list=None):
        self.user_list = []
        if screen_name_list:
            for screen_name in tqdm(screen_name_list, desc="Pulling users"):
                try: 
                    user = api.get_user(screen_name = screen_name)
                    self.user_list.append(user)
                except Exception as e:
                    print(f"{screen_name, e}")
                    continue
        elif user_id_list:
            for user_id in tqdm(user_id_list, desc="Pulling users"):
                try:
                    user = api.get_user(user_id = user_id)
                    self.user_list.append(user)
                except Exception as e:
                    print(f"{user_id, e}")
                    continue
        self.user_df = pd.DataFrame()
        for user in self.user_list:
            flat_user = pd.json_normalize(user._json)
            self.user_df = pd.concat([self.user_df, flat_user], ignore_index = True)

class Follower_ids:
    def __init__(self, screen_name):
        try:
            self.user = get_user_single(screen_name)
            self.follower_ids_list = []
            for page in tweepy.Cursor(api.get_follower_ids, user_id=self.user.id, stringify_ids=True).pages():
                self.follower_ids_list.extend(page)
            self.follower_ids_df  = pd.DataFrame(self.follower_ids_list, columns=["follower_id"])
            self.follower_ids_df.insert(0, "screen_name", self.user.screen_name)
            self.follower_ids_df.insert(1, "twitter_id", self.user.id_str)
        except Exception as e:
            print(f"{screen_name, e}")
            logging.error(f"{screen_name, e}")
            pass

class Friend_ids:
    def __init__(self, screen_name):
        try:
            self.user = get_user_single(screen_name)
            self.friend_ids_list = []
            for page in tweepy.Cursor(api.get_friend_ids, user_id=self.user.id, stringify_ids=True).pages():
                self.friend_ids_list.extend(page)
            self.friend_ids_df  = pd.DataFrame(self.friend_ids_list, columns=["friend_id"])
            self.friend_ids_df.insert(0, "screen_name", self.user.screen_name)
            self.friend_ids_df.insert(1, "twitter_id", self.user.id_str)
        except Exception as e:
            print(f"{screen_name, e}")
            logging.error(f"{screen_name, e}")
            pass

class Followers_complete:
    def __init__(self, screen_name):
        self.followers_df = pd.DataFrame()
        self.user = get_user_single(screen_name)
        for item in tqdm(tweepy.Cursor(api.get_followers, user_id=self.user.id, count=200).items(), desc="Pulling followers"):
            temp_df = pd.json_normalize(item._json)
            self.followers_df = pd.concat([self.followers_df, temp_df], ignore_index=True)

class Friends_complete:
    def __init__(self, screen_name):
        self.friends_df = pd.DataFrame()
        self.user = get_user_single(screen_name)
        for item in tqdm(tweepy.Cursor(api.get_friends, user_id=self.user.id, count=200).items(), desc="Pulling friends"):
            temp_df = pd.json_normalize(item._json)
            self.friends_df = pd.concat([self.friends_df, temp_df], ignore_index=True)

class Friend_network:
    def __init__(self, screen_name_list):
        self.user_list = User_list(screen_name_list = screen_name_list).user_list
        self.network_df = pd.DataFrame()
        for user in tqdm(self.user_list , desc="Pulling network data"):
            temp_df = Friend_ids(user.screen_name).friend_ids_df
            self.network_df = pd.concat([self.network_df, temp_df], ignore_index=True)

        screen_name_dict = {}
        follower_dict = {}
        for user in self.user_list:
            screen_name_dict.update({user.id_str: user.screen_name})
            follower_dict.update({user.id_str: user.followers_count})
        
        self.network_df["friend_name"] = self.network_df["friend_id"].map(screen_name_dict)
        self.network_df["followers_count"] = self.network_df["twitter_id"].map(follower_dict)

class User_timeline:
    def __init__(self, screen_name, start_date, end_date, exclude_replies, include_rts):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)
        self.user = get_user_single(screen_name)

        self.timeline = []
        for i in tqdm(tweepy.Cursor(api.user_timeline, user_id = self.user.id, exclude_replies = exclude_replies, include_rts = include_rts).items(), desc="Pulling user timeline"):
            if i.created_at > self.end_date:
                pass
            if i.created_at <= self.end_date and i.created_at >= self.start_date:
                self.timeline.append(i)
            if i.created_at < self.start_date:
                break

        self.timeline_df = pd.DataFrame()
        for tweet in self.timeline:
            temp_df = pd.json_normalize(tweet._json)
            temp_df.insert(0, "account", screen_name)
            self.timeline_df = pd.concat([self.timeline_df, temp_df], ignore_index=True)

class Retweeters:
    def __init__(self, status_id):
        self.retweeter_list = []
        for page in tweepy.Paginator(client.get_retweeters, id = status_id):
            if page.data:
                self.retweeter_list.extend(page.data)
        self.retweeter_id_list = [str(x.id) for x in self.retweeter_list]

class Liking_users:
    def __init__(self, status_id):
        self.liking_users_list = []
        for page in tweepy.Paginator(client.get_liking_users, id = status_id):
            if page.data:
                self.liking_users_list.extend(page.data)
        self.liking_user_id_list = [str(x.id) for x in self.liking_users_list]

class Twitter_list:
    def __init__(self, list_id):
        self.twitter_list = api.get_list(list_id=list_id)
        self.list_members_df = pd.DataFrame()
        for item in tqdm(tweepy.Cursor(api.get_list_members, list_id=list_id).items(), desc="Pulling list members"):
            temp_df = pd.json_normalize(item._json)
            self.list_members_df = pd.concat([self.list_members_df, temp_df], ignore_index=True)
