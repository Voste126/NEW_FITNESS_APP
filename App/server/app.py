from flask import Flask, request, jsonify, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db,User, Exercise, Workout
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
)
import os
from flask_cors import CORS
from sqlalchemy.dialects import postgresql
import psycopg2


load_dotenv()

app = Flask(__name__,
            static_folder='../client/build',
            template_folder='../client/build'
            )
CORS(app)

# Update the SQLAlchemy configuration to use PostgreSQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://steve:steve24@localhost:5432/fitness_tracker'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')

# Initialize SQLAlchemy, JWT, and Migrate

migrate = Migrate(app, db)
jwt = JWTManager(app)
db.init_app(app)
jwt.init_app(app)

# User registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_email = data.get('user_email')  # Get user_email from the request data
    user_phone_number = data.get('user_phone_number')  # Get user_phone_number from the request data

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Create a new user with user_email and user_phone_number
    user = User(username=username, password=password, user_email=user_email, user_phone_number=user_phone_number)

    # Validate the user data, including email and phone number if needed
    # You can add validation logic here

    db.session.add(user)
    db.session.commit()

    # Generate an access token for the newly registered user
    access_token = create_access_token(identity=username)
    # Create a redirection URL to the login page
    redirect_url = url_for('login')

    return jsonify(access_token=access_token, redirect=redirect_url), 201


#authentication when the user refreshes the page 
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    return jsonify(access_token=access_token), 200

#logging a user with authentication 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.check_password(password):
        access_token = create_access_token(identity=username)

        # Create a redirection URL to the home page
        redirect_url = url_for('home')

        return jsonify(access_token=access_token, redirect=redirect_url), 200
    else:
        return jsonify({'message': 'Invalid password'}), 401


#home page 
@app.route('/home')
def home():
    print("hello welcome to Fintech HomeWorks")
    return "Welcome to the Fintech HomeWorks"  # Return a valid response

    
# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    try:
        db.session.add(new_user)
        db.session.commit()
        response = make_response(jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201)
    except IntegrityError:
        db.session.rollback()
        response = make_response(jsonify({'error': 'Username already exists'}), 400)
    return response

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(user_list)

# Get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)
    user_data = {'id': user.id, 'username': user.username}
    return jsonify(user_data)

# Create a new workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    user_id = data.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    new_workout = Workout(date=data['date'], user_id=user_id)
    db.session.add(new_workout)
    db.session.commit()
    response = make_response(jsonify({'message': 'Workout created successfully', 'workout_id': new_workout.id}), 201)
    return response

# Get all workouts for a specific user
@app.route('/workouts/<int:user_id>', methods=['GET'])
def get_user_workouts(user_id):
    user = User.query.get(user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    workouts = Workout.query.filter_by(user_id=user_id).all()
    workout_list = [{'id': workout.id, 'date': workout.date} for workout in workouts]
    return jsonify(workout_list)

# Create a new exercise for a workout
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    workout_id = data.get('workout_id')
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)

    new_exercise = Exercise(
        name=data['name'],
        duration_minutes=data.get('duration_minutes'),
        distance_km=data.get('distance_km'),
        sets=data.get('sets'),
        reps=data.get('reps'),
        weight_kg=data.get('weight_kg'),
        category=data['category'],
        workout_id=workout_id
    )

    db.session.add(new_exercise)
    db.session.commit()
    response = make_response(jsonify({'message': 'Exercise created successfully', 'exercise_id': new_exercise.id}), 201)
    return response

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000,debug=True)
    

