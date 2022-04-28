from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"<User = {self.username}, {self.email}>"


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Listing: {self.id}, {self.timestamp}, {self.title}, {self.description}, {self.user_id}>"
