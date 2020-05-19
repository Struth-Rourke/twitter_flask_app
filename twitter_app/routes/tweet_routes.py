# twitter_app/routes/tweet_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect

from twitter_app.models import Tweets, db

tweet_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/tweets.json")
@tweet_routes.route("/tweets_endpoint")
def list_tweets():
    tweets = [
        {"id": 1, "tweet": "Hello World 1"},
        {"id": 1, "tweet": "Hello World 2"},
        {"id": 1, "tweet": "Hello World 3"},
        {"id": 2, "tweet": "Hello World 1"},
        {"id": 2, "tweet": "Hello World 2"},
        {"id": 2, "tweet": "Hello World 3"}
    ]
    return jsonify(tweets)


@tweet_routes.route("/tweets")
def list_tweets_for_humans():
    
    tweet_records = Tweets.query.all()
    print(tweet_records)

    return render_template("tweets.html", 
                           message="Here's some tweets:", 
                           tweets=tweet_records)


@tweet_routes.route("/tweets/new")
def new_tweet():
    return render_template("new_tweets.html")


@tweet_routes.route("/tweets/create", methods=["POST"])
def create_tweets():
    # Transforming the request.form into a dictionary 
    print("FORM DATA:", dict(request.form))

    # Creating a "new_tweet" instance 
    new_tweet = Tweets(tweet=request.form["tweets.tweet"], 
                       twitter_handle=request.form["twitter_handle"])
    # Adding the "new_tweet" instance to the DataBase
    db.session.add(new_tweet)
    # Committing the change to the DataBase
    db.session.commit()
    
    return redirect("/tweets")
