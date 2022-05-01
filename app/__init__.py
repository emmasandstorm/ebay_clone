from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

myobj = Flask(__name__)
myobj.config.from_mapping(
    SECRET_KEY="you-will-never-guess",
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir, "app.db"),
    UPLOAD_FOLDER='app/static/images',
    MAX_CONTENT_LENGTH = 5*1024*1024
)

db = SQLAlchemy(myobj)

from app import routes
