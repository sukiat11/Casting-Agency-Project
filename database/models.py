import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app): #, database_path=database_path
  with app.app_context():
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Actors(db.Model):
    __tablename__ = "actors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

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
