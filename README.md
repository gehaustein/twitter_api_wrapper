# This package is meant to provide easy-to-read wrappers for perfoming common Twitter API tasks

## Prerequisites:
The following code runs on <span style="color:darkred">**Python 3.9**</span>
1. Create and activate a new conda environment by running the following in your terminal:\
<code>conda create python=3.9 -n NAME-YOUR-ENV</code>\
<code>conda activate NAME-YOUR-ENV</code>
2. Install the Python package with all necessary requirements using:\
<code>pip install git+https://github.com/ckdata/Tweepy_basics.git</code>

## Configuration
We are using a config.ini to deal with authentification. This is more secure and allows us to share code securely without sharing any keys needed to access the Twitter API.
1. Create a config.ini file ideally by either:\
*Option A:* right-click in VS Code, new file and name it "config.ini". \
*Option B:* navigate to the current directory in a terminal and enter <code>touch config.ini</code>.
2. Use the following format to store the Twitter API credential in your your config.ini:\
<code>[TWITTER]</code>\
<code>TWITTER_C_KEY=...</code>\
<code>TWITTER_C_SECRET=...</code>\
<code>TWITTER_A_KEY=...</code>\
<code>TWITTER_A_SECRET=...</code>
3. Enter the Twitter API credentials by either:\
*Option A:* open the config.ini in your code editor, enter your credentials and save it.\
*Option B:* open the config.ini in your terminal by entering <code>open config.ini</code> while in the working directory.

## Usage
* <code>get_user_single</code>: returns a JSON-like user object for a screen name directly from the API
* <code>User_list</code>: user objects for a list of screen names or user ids
    * <code>.user_list</code>: list of user objects
    * <code>.user_df</code>: API output in flat format
* <code>Follower_ids</code>: follower ids for a given screen name
    * <code>.user</code>: JSON-like user object of the input user
    * <code>.friend_ids_list</code>: list of all user ids of followers
    * <code>.friend_ids_df</code>: data frame containing user ids of followers with screen name and user id of input user
* <code>Friend_ids</code>: friend ids for a given screen name
    * <code>.user</code>: JSON-like user object of the input user
    * <code>.friend_ids_list</code>: list of all user ids of friends
    * <code>.friend_ids_df</code>: data frame containing user ids of friends with screen name and user id of input user
* <code>Followers_complete</code>: complete information on Followers
    * <code>.user</code>: JSON-like user object of the input user
    * <code>.followers_df</code>: data frame containing detailed information on followers
* <code>Friends_complete</code>: complete information on friends
    * <code>.user</code>: JSON-like user object of the input user
    * <code>.friends_df</code>: data frame containing detailed information on friends
* <code>Friend_network</code>: input data to generate a network of users in R
    * <code>.user_list</code>: list of user objects
    * <code>.network_df</code>: data frame which can be transferred to R or kept for further analysis
* <code>User_timeline</code>: all activities for a user within a given timeframe
    * <code>.start_date</code>: datetime object of the given start date
    * <code>.end_date</code>: datetime object of the given end date
    * <code>.user</code>: JSON-like user object of the input user
    * <code>.timeline_df</code>: data frame containing all activities in a given user's timeline
* <code>Retweeter_ids</code>: lookup user which retweeted a given tweet identified by its id
    * <code>.retweeter_list</code>: list of users which retweeted a tweet


