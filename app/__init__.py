import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Initialize application
app = Flask(__name__, static_folder=None)

# Enabling cors
CORS(app)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize Flask Sql Alchemy
db = SQLAlchemy(app)

# Import the application views
from app import views

# Register blue prints
from app.auth.views import auth

app.register_blueprint(auth, url_prefix='/v1')

from app.item.views import item

app.register_blueprint(item, url_prefix='/v1')

from app.variant.views import variant

app.register_blueprint(variant, url_prefix='/v1')

from app.userAction.views import useraction

app.register_blueprint(useraction, url_prefix='/v1')
