# twitter_app/__init__.py

# Importing Flask that allows you to make the app
from flask import Flask

# Importing necessary classes, packages, , routes, etc.
from twitter_app.models import db, migrate
from twitter_app.routes.home_routes import home_routes
from twitter_app.routes.tweet_routes import tweet_routes
from twitter_app.routes.twitter_routes import twitter_routes


# DataBase File Path
DATABASE_URI = "sqlite:///twitter_flask_app_db.db" # using relative filepath
#DATABASE_URI = "sqlite://///Users/rourkestruthers/Desktop/ComputerScience/LambdaSchool/Unit3-DataEngineering/Sprint3-Productization_Cloud/DS-Unit-3-Sprint-3-Productization-and-Cloud/twitter_flask_app/twitter_flask_app_db.db" # using absolute filepath on Mac (recommended)


# Instiailizing the app inside of a function
def create_app():
    # Instantiating Flask App
    app = Flask(__name__)

    # Configures the DataBase
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    # Initializes the DataBase
    db.init_app(app)
    # Migrates the app and DataBase
    migrate.init_app(app, db)

    # Registering the blueprints for the different app routes
    app.register_blueprint(home_routes)
    app.register_blueprint(tweet_routes)
    app.register_blueprint(twitter_routes)
    
    # Returning / Running Flask App
    return app





# Factory pattern; Flask best practice
if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)