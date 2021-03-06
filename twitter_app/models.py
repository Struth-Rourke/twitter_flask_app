# twitter_app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instantiating the DataBase from the SQLAlchemy Class
db = SQLAlchemy()

# Instantiating Migrate
migrate = Migrate()

# Defining new class "Tweets": inherents db.model from SQLAlchemy above
class Tweets(db.Model):
    ###__table_name__ = "tweet_table" #> configuing table name
    # Configuring the attributes, and subsequent DB columns
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"))
    twitter_handle = db.Column(db.String(128))
    full_text = db.Column(db.String(128))
    embedding = db.Column(db.PickleType)

    # bi-directional association with User model
    user = db.relationship("User", backref=db.backref("tweets", lazy=True))

# Defining new class "User": inherents db.model from SQLAlchemy above
class User(db.Model):
    # Configuring attributes, and subsequent DB columns 
    id = db.Column(db.BigInteger, primary_key=True)
    screen_name = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String)
    location = db.Column(db.String)
    followers_count = db.Column(db.Integer)
    #latest_tweet_id = db.Column(db.BigInteger)


# Defining the parse_records function
def parse_records(database_records):
    """
    A helper method for converting a list of database record objects into a list 
    of dictionaries, so they can be returned as JSON.

    Param: database_records (a list of db.Model instances)

    Example: parse_records(User.query.all())

    Returns: a list of dictionaries, each corresponding to a record, like...
        [
            {"id": 1, "title": "Book 1"},
            {"id": 2, "title": "Book 2"},
            {"id": 3, "title": "Book 3"},
        ]
    """
    parsed_records = []
    for record in database_records:
        print(record)
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records
