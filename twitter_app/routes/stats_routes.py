# web_app/routes/stats_routes.py

##------------------------------------------------------------------------------
# 1. Importing specified packages 
##------------------------------------------------------------------------------

### flask ###

## Blueprint: 
# "blueprint" or paradigm of how to construct or extend an app
from flask import Blueprint
## request: remembers the matched endpoint and view arguments; 
# request.form: the key/value pairs in an HTML form body that isn't JSON encoded
from flask import request 
## render_template: renders an HTML template;
# provide the name of the template and the variables you want to pass to the 
# template engine as keyword arguments
from flask import render_template

### APIs / Connection Objects ###

# Basilica API Connection (Object / Method)
from twitter_app.services.basilica_service import basilica_conn
# Tweets and User (Classes)
from twitter_app.models import Tweets, User

# SKLearn
from sklearn.linear_model import LogisticRegression


##------------------------------------------------------------------------------
# 2. Setting Blueprint; Defining Function and Variables 
##------------------------------------------------------------------------------

# Blueprint: attribute "stats_routes" refers to the .py file for __init__ IDing;
# set equal to "stats_routes" so we can register the blueprint in the __init__ file
stats_routes = Blueprint("stats_routes", __name__)

# Decorator: ".route" to a particular page of the app; 
# blueprint will record the intention of registering the function 
@stats_routes.route("/predict", methods=["POST"])
# Function: "predict"
def predict():
    #print("PREDICT ROUTE...")
    # Creating a dictionary from the requested HTML form
    print("FORM DATA:", dict(request.form))
    #> {'screen_name_a': 'wolfejosh', 'screen_name_b': 'paulg', 'tweet_text': 'Example tweet text here'}
    
    # Variables that are requested from the specific form "name" ("screen_name_a")
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    # Tweet Text variable that is requested from the specific form name ("tweet_text")
    tweet_text = request.form["tweet_text"]


##------------------------------------------------------------------------------
# 3. Querying the SQL DataBase
##------------------------------------------------------------------------------


    print("-----------------")
    print("FETCHING TWEETS FROM DATABASE...")
    # TODO: wrap in a try block in case the user's don't exist in the database

    # Mock query if we couldn't use flask-sqlalchemy
    # "SELECT * FROM users WHERE screen_name = {screen_name_a}"

    # Querying the screen_name via the User class, and IDing as "screen_name_x"
    # as per the HTML form -- pulling only ".one" 
    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()
    # Grabbing the tweets assoicated with the specified "user_x" from above
    user_a_tweets = user_a.tweets 
    user_b_tweets = user_b.tweets

    # Could choose to grab the particular embedding instead of actual tweet
    #user_a_embeddings = [tweet.embedding for tweet in user_a_tweets]
    #user_b_embeddings = [tweet.embedding for tweet in user_b_tweets]
    
    # Printing the user_x screen_name and "len" (number) of tweets in the DB
    # can reference the tweets attribute since user_x is of the User class
    print("USER A", user_a.screen_name, len(user_a.tweets))
    print("USER B", user_b.screen_name, len(user_b.tweets))


##------------------------------------------------------------------------------
# 4. Model Training 
##------------------------------------------------------------------------------


    print("-----------------")
    print("TRAINING THE MODEL...")
    
    ## Define empty lists -- used in modeling later on
    # embeddings = X Feature Matrix
    embeddings = []
    # labels = y target vector
    labels = []
    
    ## For Loops: 
    # appending user_x screen_name, and tweet.embeddings, to enpty lists
    for tweet in user_a_tweets:
        labels.append(user_a.screen_name)
        embeddings.append(tweet.embedding)

    for tweet in user_b_tweets:
        labels.append(user_b.screen_name)
        embeddings.append(tweet.embedding)

    # Instantiating and Fitting Model to (X, y)
    classifier = LogisticRegression()
    classifier.fit(embeddings, labels)


##------------------------------------------------------------------------------
# 5. Model Prediction
##------------------------------------------------------------------------------


    print("-----------------")
    print("MAKING A PREDICTION...")
    # result_a = classifier.predict([user_a_tweets[0].embedding])
    # result_b = classifier.predict([user_b_tweets[0].embedding])

    # Setting Variable to basilica connection object to reference embeddings
    basilica_api = basilica_conn
    
    # Example embedding using basilica "twitter" NLP model 
    example_embedding = basilica_api.embed_sentence(tweet_text, model="twitter")
    
    # Result = model prediction based on example embedding
    result = classifier.predict([example_embedding])
    

##------------------------------------------------------------------------------
# 6. Return Rendered Template
##------------------------------------------------------------------------------

    # Rendered HTML Template w/ specified attributes
    return render_template("prediction_results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely= result[0]
    )
