import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.sql import func
from datetime import datetime

# database_path = os.environ['DATABASE_URL']
# if database_path.startswith("postgres://"):
#   database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app): #, database_path=database_path
  with app.app_context():
    # app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    
    # # add one demo row which is helping in POSTMAN test
    # drink = Drink(
    #     title='water',
    #     recipe='[{"name": "water", "color": "blue", "parts": 1}]'
    # )

    # drink.insert()
    

# class Person(db.Model):  
#   __tablename__ = 'People'

#   id = Column(db.Integer, primary_key=True)
#   name = Column(String)
#   catchphrase = Column(String)

#   def __init__(self, name, catchphrase=""):
#     self.name = name
#     self.catchphrase = catchphrase

#   def format(self):
#     return {
#       'id': self.id,
#       'name': self.name,
#       'catchphrase': self.catchphrase}

class Actors(db.Model):
    __tablename__ = "actors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    
    # def __init__(self, name, age, gender):
    #     self.name = name
    #     self.age = age
    #     self.gender = gender
      
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
        }
    
class Movies(db.Model):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    
    # def __init__(self, title, release_date):
    #     self.title = title
    #     self.release_date = release_date
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date
        }
