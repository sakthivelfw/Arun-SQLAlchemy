import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

# Inserting data into user db
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name",
       type=str,
       required=True,
       help="User name cannot be blank",
    )

    parser.add_argument("password",
       type=str,
       required=True,
       help="password name cannot be blank",
    )
    
    def post(self):
         data = UserRegister.parser.parse_args()
         
         #check whether username already exists or not
         if UserModel.findby_username(data['name']):
             return {'message': '{} already exists'.format(data['name'])}, 400

         saveuser = UserModel(**data)
         saveuser.save_to_db()
         
         return {"message": "User created successfully"}, 201

    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}