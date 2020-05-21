# twitter_app/routes/test_routes.py

##------------------------------------------------------------------------------
# 1. Importing specified packages 
##------------------------------------------------------------------------------

from flask import Blueprint, render_template, jsonify, request
from twitter_app.services.twitter_service import api as twitter_api
from twitter_app.services.basilica_service import basilica_conn
from twitter_app.models import Tweets, User, db


##------------------------------------------------------------------------------
# 2. Setting Blueprint; Defining Function and Variables 
##------------------------------------------------------------------------------

# Blueprint
test_routes = Blueprint("test_routes", __name__)

# Decorator
@test_routes.route("/test_users")
# Function
def list_users_human_friendly():
    db_users = User.query.all()
    return render_template("users.html", users=db_users)

# @test_routes.route("/test_users")
# def add_users():
