from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User = {self.username}, {self.email}>"


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    for_purchase = db.Column(db.Boolean, default=False)
    purchase_price = db.Column(
        db.Integer
    )  # Dollars only, working with cents presents too many questions
    for_auction = db.Column(db.Boolean, default=False)
    auction_end = db.Column(db.DateTime)

    # bids
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Listing: {self.id}, {self.timestamp}, {self.title}, {self.description}, {self.user_id}>"
