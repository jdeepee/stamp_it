from flask import Flask, render_template, flash, request, url_for, redirect, session, send_file, Response, jsonify, abort #Importing flask modules
from flask_restful import Resource, Api #Importing flask rest modules
from functools import wraps #Importing a wrapping function to validate endpoints for data
from werkzeug.debug import get_current_traceback #Importing a libary to get traceback for when I am debugging
from werkzeug.utils import secure_filename #Secure filename for creating a unique filename
from werkzeug import secure_filename #Same as before
from datetime import datetime, timedelta #Importing a time module to assign dates to posts

import json, requests, time, jwt, traceback, uuid, os, boto, uuid, gc#Other imports

from datetime import datetime 
from datetime import timedelta

from uuid import UUID

application = Flask(__name__) #Creating application
api = Api(application) #Creating application

from . import config

from .db.database_model import *

db.init_app(application)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
session._model_changes = {}

from .routes.users import *
from .routes.users_auth import *
from .routes.loops import *
from .routes.loops_auth import *
from .routes.index import *
from .routes.custom_loops import * 

##############################################################
						#Other
##############################################################

api.add_resource(Home, '/')
api.add_resource(PostCheck, '/post_check/')
api.add_resource(S3Check, '/s3check/')
# api.add_resource(NLP, '/suggestedimage/')

##############################################################
						#users
##############################################################

api.add_resource(UserSignUp, '/users/') #POST 
api.add_resource(UserSearch, '/users/search/') #GET
api.add_resource(UserProfile, '/users/<id>/') #GET
api.add_resource(UserPosts, '/users/<id>/posts/') #GET
api.add_resource(AuthToken, '/authtoken/') #POST
api.add_resource(UserCheck, '/usernamecheck/') #GET

##############################################################
						#users_jwt
##############################################################

api.add_resource(UserChange, '/users/<uuid:id>/') #PATCH, DELETE
api.add_resource(UserSavedStories, '/users/<id>/savedstories/') #GET, POST

##############################################################
						#stories
##############################################################

api.add_resource(NearbyLoops, '/loops/nearby/') #GET
api.add_resource(SearchLoops, '/loops/search/') #GET
api.add_resource(LoopsPosts, '/loops/<id>/') #GET
api.add_resource(Trending, '/trending/')

##############################################################
						#stories_jwt
##############################################################

api.add_resource(PostToLoop, '/loops/<id>/') #POST
api.add_resource(VotePost, '/post/<id>/vote/') #POST, DELETE
api.add_resource(DeletePost, '/post/<id>/') #DELETE

##############################################################
						#custom_loops
##############################################################

api.add_resource(CreateLoop, '/loops/create/')
api.add_resource(ConfirmLoop , '/loops/<id>/confirm/')
