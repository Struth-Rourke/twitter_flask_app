# twitter_app/routes/twitter_routes.py

# Importing necessary packages and dependencies from other areas of the directory
from flask import Blueprint, render_template, jsonify, request
from twitter_app.services.twitter_service import api as twitter_api
from twitter_app.services.basilica_service import bacilica_API_conn
from twitter_app.models import Tweets, User, db
from pprint import pprint


# Creating twitter_routes blueprint
twitter_routes = Blueprint("twitter_routes", __name__)

# Defining the "get_user" function
@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)
    
    # Getting the twitter user, via twitter_api w/ "get_user" method
    twitter_user = twitter_api.get_user(screen_name)
    # Getting the users timeline w/ "user_timeline" method
    statuses = twitter_api.user_timeline(screen_name, tweet_mode="extended", 
                                         count=150, exclude_replies=True, 
                                         include_rts=False)


    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    
    
    basilica_api = bacilica_API_conn


    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS:", len(embeddings))

    # TODO: explore using the zip() function maybe...
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        #print(dir(status))
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweets.query.get(status.id) or Tweets(id=status.id)
        db_tweet.user_id = status.user.id # or db_user.id
        db_tweet.full_text = status.full_text
        #embedding = basilica_client.embed_sentence(status.full_text, model="twitter") # todo: prefer to make a single request to basilica with all the tweet texts, instead of a request per tweet
        db_tweet.embedding = embeddings[counter]
        db.session.add(db_tweet)
        counter+=1
    
    db.session.commit()
    
    
    #breakpoint()
    return "OK"
    #return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets
    
