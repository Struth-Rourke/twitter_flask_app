#twitter_flask_app


#Running App
# FLASK_APP=twitter_app flask run


#Creating DB
#> generates app/migrations dir
# FLASK_APP=twitter_app flask db init 

##Migrating and Upgrading DB for changes
#run both when changing the schema:
#> creates the db (with "alembic_version" table)
# FLASK_APP=twitter_app flask db migrate 

#> creates the specified tables
# FLASK_APP=twitter_app flask db upgrade 




# Heroku App Name:
# twitter-prediction-flask-app
# https://twitter-prediction-flask-app.herokuapp.com/ 