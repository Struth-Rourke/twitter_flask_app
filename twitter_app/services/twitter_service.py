import os
import tweepy
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

# Twitter Credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


# Authorization Information(.env) -- via Tweepy package
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
print("AUTH:", auth)

# API via auth keys
api = tweepy.API(auth)
print("API:", api)
#print(dir(api))


# Wrapper Function
# def twitter_api():
#     auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
#     auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
#     print("AUTH", auth)
#     api = tweepy.API(auth)
#     print("API", api)
#     #print(dir(api))
#     return api


if __name__ == "__main__":
    
    # Getting information from a specific user
    # user = api.get_user("rourke_robert_")
    #> <class 'tweepy.models.User>

    # pprint(user._json)
    # print(user.id)
    # print(user.screen_name)
    # print(user.friends_count)
    # print(user.followers_count)


    # Getting tweets from a specified given user
    statuses = api.user_timeline("rourke_robert_", 
                                 tweet_mode="extended", 
                                 count=150, 
                                 exclude_replies=True, 
                                 include_rts=False)
    
    #print(type(statuses)) #> 
    # status = statuses[0]
    # pprint(dir(status))
    # print(status.id)
    # print(status.full_text)

    # For loop to retrieve all the tweets w/ full text
    for status in statuses:
        print("-----")
        print(status.full_text)











    # api = twitter_api()
    # user = api.get_user("elonmusk")
    # print("USER", user)
    # print(user.screen_name)
    # print(user.name)
    # print(user.followers_count)

    #breakpoint()

    #public_tweets = api.home_timeline()
    #
    #for tweet in public_tweets:
    #    print(type(tweet)) #> <class 'tweepy.models.Status'>
    #    #print(dir(tweet))
    #    print(tweet.text)
    #    print("-------------")