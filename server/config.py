
# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
# from flask_wtf.csrf import CSRFProtect
# from flask_jwt_extended import JWTManager
# from dotenv import load_dotenv

# # Load environment variables from .env
# load_dotenv()

# class Config:
#     # Your secret key for session management and CSRF protection
#     SECRET_KEY = os.environ.get('SECRET_KEY') 

#     # Database configuration
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking

# app = Flask(__name__)

# # Load configuration from the Config class
# app.config.from_object(Config)

# # Initialize SQLAlchemy and Migrate
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# jwt = JWTManager(app)

# # Enabling CORS on the Flask app instance
# CORS(app)

# # Initialize CSRF protection
# csrf = CSRFProtect(app)

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import psycopg2
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# loads environment variables from .env
load_dotenv()

# app initialization
app = Flask(__name__)

# configuring for postgres
app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# intializing SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# associate SQLAlchemy db with the flask app
# db.init_app(app)

# enabling CORS on the Flask app instance
CORS(app)

# secret key for sessions here
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# initialize CSRF protection
csrf = CSRFProtect(app)
