import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def json(self):
        return {'name': self.name, 'password': self.password}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def findby_username(cls,name):
        return cls.query.filter_by(name=name).first()
        
    
    @classmethod
    def findby_id(cls,_id):
        return cls.query.filter_by(_id=id).first()