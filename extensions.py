"""This file contains the extensions used in the application."""

from flask_sqlalchemy import SQLAlchemy#SQLAlchemy database engine.
from flask_admin import Admin#Extension to manage the admin page.
from flask_bcrypt import Bcrypt

db=SQLAlchemy()#Instance of SQLAlchemy.
admin=Admin()#Instance of admin.
encrypt=Bcrypt()#Instance of bcrypt password hashin utility