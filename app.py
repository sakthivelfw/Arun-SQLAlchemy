import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, get_identity
from resource.userObject import UserRegister
from resource.items import UpdateList, postList, Items, Items_List
from resource.stores import Stores, StoreList
from db import db
    
app = Flask(__name__)
app.secret_key = "akai"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///user.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

jwt = JWT(app,authenticate,get_identity) # doing this we will get auth token where the /auth is an endpoint created by JWT by default

api.add_resource(UpdateList, '/itemUpdate') # Put insert or update
api.add_resource(postList, '/insert_item') # Post item
api.add_resource(Items, '/item/<string:name>') #Get & Delete
api.add_resource(Items_List, '/items')
api.add_resource(StoreList, '/getallStores')
api.add_resource(Stores, '/getStores')
api.add_resource(UserRegister, '/signup_users')

if __name__ == "__main__":
    app.run(port=4999, debug=True) #setting debug = true will let the api developer know what goes wrong