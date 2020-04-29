from flask_restful import Resource, reqparse  #important to import reqparse
from flask_jwt import JWT, jwt_required #JWT is used to create a token for auth purpose
from flask import Flask, request
import sqlite3
from models.items import ItemModel

items = []

class RequestJsonParser():
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='price cannot be blank')
    parser.add_argument('name', required=True, help='name cannot be blank')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs storeid')


class Items(Resource):
    @jwt_required()
    def get(self, name):
        #item_list = next(filter(lambda x: x['name'] == name, items), None) # iter is not required above python 3

        #getting items from DB
        item = ItemModel.getitemname(name)
        if item:
            return item.json(), 200

        return {'message': "No item found"}, 404

    def delete(self,name):
        #global items
        #items = list(filter(lambda x: x['name'] != name, items))
        isItemFound = ItemModel.getitemname(name)
        
        if isItemFound:
            isItemFound.delete_from_db()
        
        return {'message': 'Requested item deleted'}
            


class postList(Resource):
    def post(self):
        requestData = RequestJsonParser.parser.parse_args() #this is required to get the data from mobile or frond end where we pass as a parameter

        if ItemModel.getitemname(requestData['name']):
            return {'message': "An item with name '{}' already exists.".format(requestData['name'])}, 400

        itemList = ItemModel(**requestData)

        try:
            itemList.save_to_db()
        except:
            return {'message', 'failed to insert item'}, 500

        return itemList.json(), 201 #adding code 201 is used when data is created


class UpdateList(Resource):
    def put(self):
        requestData = RequestJsonParser.parser.parse_args()
        item = ItemModel.getitemname(requestData['name'])
        #updated_item = {"name": requestData['name'], "price": requestData["price"]}
       
        if item is None:
            item = ItemModel(**requestData)
        else:
            item.price = requestData["price"]
            item.name = requestData["name"]
            item.store_id = requestData['store_id']

        item.save_to_db()

        return item.json()


class Items_List(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
