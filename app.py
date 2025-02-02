#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
# from flask_wtf import Form
#from models import db, Artist, Venue, Show
from utils import *
from database.models import db, setup_db, db_drop_and_create_all, Actors, Movies
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(test_config=None):

    app = Flask(__name__)
    moment = Moment(app)
    app.config.from_object('config')
    setup_db(app)
    
    # Set up migration
    migrate = Migrate(app, db)
    
    # Set up Filters.
    app.jinja_env.filters['datetime'] = format_datetime
    
    CORS(app)

    return app

app = create_app()

# # To reset the database
# with app.app_context():
#     db_drop_and_create_all()
    
#----------------------------------------------------------------------------#
# Actors
#----------------------------------------------------------------------------#

@app.route('/actors', methods=['GET'])
# @requires_auth('get:actors')
def get_actors():
    # Get all actors in the database
    try:
        actors = Actors.query.all()
        actors_display = [m.format() for m in actors]
            
        return jsonify({
            'success': True,
            'movies': actors_display
        }), 200
    
    except Exception as e:
        abort(500)

@app.route('/actors/<int:id>', methods=['GET'])
# @requires_auth('get:actor_by_id')
def get_actor(id):
    # Get actor based on id
    try:
        actor = Actors.query.get(id)
        
        # If it does not exist, show an error
        if not actor:
            print(f"Actor with id {id} not found.")
            abort(404)
            
        return jsonify({
            'success': True,
            'movies': actor.format()
        }), 200
    
    except Exception as e:
        abort(500)
        
@app.route('/actors/add', methods=['POST'])
def add_actor():
    # Add actor to database
    body = request.get_json()
    
    if "name" not in body.keys() or "age" not in body.keys() or "gender" not in body.keys():
        abort(422)
        
    name = body['name']
    age = body['age']
    gender = body['gender']
    
    try:
        # Create new actor object
        new_actor = Actors(name=name, age=age, gender=gender)
        new_actor.insert()
        
        return jsonify({
            "success": True,
            "actor": new_actor.format()
        }), 200
        
    except Exception as e:
        print(e)
        abort(500)
    
    
@app.route('/actors/<int:id>', methods=['PATCH'])
# @requires_auth('patch:actors')
def update_actor(id):
    # Update actor in database based on id
    body = request.get_json()
    
    try:
        # Check if it exists in the database
        actor = Actors.query.get(id)
        
        # If it does not exist, show an error
        if not actor:
            print(f"Actor with id {id} not found.")
            abort(404)
            
        if 'name' in body:
            actor.name = body['name']
        
        if 'age' in body:
            actor.age = body['age']
            
        if 'gender' in body:
            actor.gender = body['gender']
            
        # Update actor object
        actor.update()
        
        return jsonify({
            "success": True,
            "actor": actor.format()
        }), 200
        
    except Exception as e:
        print(e)
        abort(500)
    

@app.route('/actors/<int:id>', methods=['DELETE'])
# @requires_auth('delete:actors')
def delete_actor(id):
    try: 
        # Get actor object
        actor = Actors.query.get(id)

        # Object not found, nothing to delete
        if not actor:
            print(f"Actor with id {id} not found.")
            abort(404)
        
        actor.delete()
    
        return jsonify({
            "success": True,
            "delete": id
        }), 200
    except:
        abort(500)
    
#----------------------------------------------------------------------------#
# Movies
#----------------------------------------------------------------------------#

@app.route('/movies', methods=['GET'])
# @requires_auth('get:movies')
def get_movies():
    # Get all movies in the database
    try:
        movies = Movies.query.all()
        movies_display = [m.format() for m in movies]
            
        return jsonify({
            'success': True,
            'movies': movies_display
        })
    
    except Exception as e:
        abort(500)

@app.route('/movies/<int:id>', methods=['GET'])
# @requires_auth('get:movies')
def get_movie():
    # Get mopvie based on id
    try:
        movie = Movies.query.get(id)
        
        # If it does not exist, show an error
        if not movie:
            print(f"Movie with id {id} not found.")
            abort(404)
            
        return jsonify({
            'success': True,
            'movies': movie.format()
        })
    
    except Exception as e:
        abort(500)  
    
@app.route('/movies/add', methods=['POST'])
def add_movie():
    # Add movie to database
    body = request.get_json()
    
    if "title" not in body.keys() or "release_date" not in body.keys():
        abort(422)
    
    title = body['title']
    release_date = body['release_date']
    
    try:
        # Create new actor object
        new_movie = Movies(title=title, release_date=release_date)
        new_movie.insert()
        
        return jsonify({
            "success": True,
            "movie": new_movie.format()
        })
        
    except Exception as e:
        print(e)
        abort(500)
    
@app.route('/movies/<int:id>', methods=['PATCH'])
# @requires_auth('patch:movies')
def update_movie(id):
    # Update actor in database based on id
    body = request.get_json()
    
    try:
        # Check if it exists in the database
        movie = Movies.query.get(id)
        
        # If it does not exist, show an error
        if not movie:
            print(f"Movie with id {id} not found.")
            abort(404)
            
        if 'title' in body:
            movie.title = body['title']
        
        if 'release_date' in body:
            movie.release_date = body['release_date']
            
        # Update movie object
        movie.update()
        
        return jsonify({
            "success": True,
            "actor": movie.format()
        }), 200
        
    except Exception as e:
        print(e)
        abort(500)
    

@app.route('/movies/<int:id>', methods=['DELETE'])
# @requires_auth('delete:movies')
def delete_movie(id):
    try: 
        # Get movie object
        movie = Movies.query.get(id)

        # Object not found, nothing to delete
        if not movie:
            print(f"Movie with id {id} not found.")
            abort(404)
        
        movie.delete()
    
        return jsonify({
            "success": True,
            "delete": id
        }), 200
    except:
        abort(500)
    
    
#----------------------------------------------------------------------------#
# Others
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('errors/404.html'), 404

# @app.errorhandler(500)
# def server_error(error):
#     return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=8080, debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
