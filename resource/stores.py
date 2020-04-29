from flask_restful import Resource, reqparse
from models.stores import StoreModel


class RequestJsonParser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, help='name cannot be blank')

class Stores(Resource):

    def get(self):
        requestData = RequestJsonParser.parser.parse_args()
        store = StoreModel.getstorename(requestData['name'])
        if store:
            return store.json()
        return {'message': 'store not found'}

    
    def post(self):
        requestData = RequestJsonParser.parser.parse_args()
        
        if StoreModel.getstorename(requestData['name']):
            return {'message': 'Store name already exists'}

        store = StoreModel(requestData['name']) 

        try:
            store.save_to_db()
        except:
            return {'message': 'internal error has been occured'}, 500

        
        return store.json(), 201

    def delete(self):
        requestData = RequestJsonParser.parser.parse_args()
        store = StoreModel.getstorename(requestData['name'])

        if store:
            store.delete_from_db()

        return {'message': 'Store deleted from db'}


class StoreList(Resource):
    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}