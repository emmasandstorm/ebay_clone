from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search
import os

basedir = os.path.abspath(os.path.dirname(__file__))

myobj = Flask(__name__)
myobj.config.from_mapping(
    SECRET_KEY="you-will-never-guess",
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(basedir, "app.db"),
    UPLOAD_FOLDER="app/static/images",
    MAX_CONTENT_LENGTH=5 * 1024 * 1024,
)

db = SQLAlchemy(myobj)
login = LoginManager(myobj)
login.login_view = "/login"
search = Search()
search.init_app(myobj)

from app import routes
from app import exceptions
