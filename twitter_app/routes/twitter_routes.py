# twitter_app/routes/twitter_routes.py

##------------------------------------------------------------------------------
# 1. Importing specified packages 
##------------------------------------------------------------------------------

# Importing necessary flask methods
from flask import Blueprint, render_template, jsonify, request
# Importing necessary API connections 
from twitter_app.services.twitter_service import api as twitter_api
from twitter_app.services.basilica_service import basilica_conn
# "Tweets" and "User" (Classes) and "db" (SQLAlchemy()) variable 
from twitter_app.models import Tweets, User, db
# from pprint import pprint -- pretty print; makes output easier to read


##------------------------------------------------------------------------------
# 2. Setting Blueprint; Defining Function and Variables 
##------------------------------------------------------------------------------

# Blueprint: attribute "twitter_routes" refers to the .py file for __init__ IDing;
# set equal to "twitter_routes" so we can register the blueprint in the __init__ file
twitter_routes = Blueprint("twitter_routes", __name__)

# Decorator: ".route" to a particular page of the app; 
# blueprint will record the intention of registering the function 
@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)
    
    # Getting the twitter user, via twitter_api w/ "get_user" method
    twitter_user = twitter_api.get_user(screen_name)
    # Getting the users timeline w/ "user_timeline" method
    # statuses = twitter_api.user_timeline(screen_name, tweet_mode="extended", 
    #                                      count=150, exclude_replies=True, 
    #                                      include_rts=False)
    
    # Adjustment to account for RTs and Replies up to 150
    statuses = twitter_api.user_timeline(screen_name,
                                         tweet_mode="extended",
                                         count=150)


##------------------------------------------------------------------------------
# 3. Querying the SQL DataBase
##------------------------------------------------------------------------------

    # Querying existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)

    # Equating the attributes from the User Class to the Twitter_API attributes
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    
    # Adding(.add) the "db_user" equations to the DataBase and committing(save)
    db.session.add(db_user)
    db.session.commit()


##------------------------------------------------------------------------------
# 4. API Connection and Creating Tweet Embeddings
##------------------------------------------------------------------------------


    # Setting Basicilia API Connection to a variable
    basilica_api = basilica_conn

    # List Comprehension for set full_text of tweets to variable 
    all_tweet_texts = [status.full_text for status in statuses]
    # Creating embeddings for the full_text tweets via model="twitter"(basilica NLP model)
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
    # Printing the "len"(number) of embeddings
    print("NUMBER OF EMBEDDINGS:", len(embeddings))

    # TODO: explore using the zip() function maybe...
    # Setting counter for each specific tweet
    counter = 0
    ## For Loop:
    # Looping through statuses and 
    for status in statuses:
        # Printing the full-text of the tweets from the user_timeeline; 
        # specified above
        print(status.full_text)
        print("----")
        #print(dir(status))
        
        # Get existing tweet from the DataBase or initialize a new one:
        db_tweet = Tweets.query.get(status.id) or Tweets(id=status.id)
        db_tweet.user_id = status.user.id #> or db_user.id
        db_tweet.full_text = status.full_text
        #embedding = basilica_client.embed_sentence(status.full_text, model="twitter") 
        # TODO: (DONE above in "embeddings" -- instead of above code) 
        # prefer to make a single request to basilica with all the tweet texts,
        # instead of a request per tweet
        # Embedding tweets and counting them up
        db_tweet.embedding = embeddings[counter]
        # Adding(.add) the embedded tweets into the DataBase
        db.session.add(db_tweet)
        counter+=1
    # Committing(saving) to the DataBase
    db.session.commit()
    
    
    return "OK"
    #return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets
    

