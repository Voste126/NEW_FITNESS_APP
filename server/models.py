# from config import db


# class Exercise(db.Model):

#     __tablename__ = 'exercises'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.String(255))
#     sets = db.Column(db.Integer)
#     reps = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())


#     workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', lazy=True)

# class UserWorkout(db.Model):
#     __tablename__ = 'user-workouts'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# class User(db.Model):

#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), nullable=False, unique=True)
#     password = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

#     workouts = db.relationship('Workout', back_populates='user', lazy=True)

# class WorkoutExercise(db.Model):
#     __tablename__ = 'workout_exercises'

#     id = db.Column(db.Integer, primary_key=True)
#     workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
#     exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# class Workout(db.Model):

#     __tablename__ = 'workouts'

#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(255))
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, onupdate=db.func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#     user = db.relationship('User', back_populates='workouts')
#     exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', lazy=True)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt()
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # Removed unique constraint
    user_email = db.Column(db.String(120), unique=True, nullable=False)  # Added user_email
    user_phone_number = db.Column(db.String(20), unique=True, nullable=True)  # Added user_phone_number
    workouts = db.relationship('Workout', backref='user', lazy=True)

    @validates
    def validate_password(self, password):
        if len(password) < 6 or len(password) > 60:
            raise ValueError("Password must be between 6 and 60 characters")

        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one capital letter")

        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r'[0-9]', password):  # Added requirement for a digit
            raise ValueError("Password must contain at least one digit")

        if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password):
            raise ValueError("Password must contain at least one special character")
    

    def __init__(self, username, password, user_email, user_phone_number):
        self.username = username
        self.password = self.generate_password_hash(password)
        self.user_email = user_email
        self.user_phone_number = user_phone_number


    def generate_password_hash(self, password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercises = db.relationship('Exercise', backref='workout', lazy=True)


# Each workout can have multiple exercises.
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)
    distance_km = db.Column(db.Float, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(50), nullable=False) 
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
