from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    user_profile = db.Column(db.String(256))
    
    collection = db.relationship("Listing", backref="buyer", lazy="dynamic")
    bids = db.relationship("Bid", backref="bidder", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User = {self.username}>"


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    seller_id = db.Column(db.Integer)
    image = db.Column(
        db.String(256)
    )  # store the file name since all images are in the same directory
    
    for_purchase = db.Column(db.Boolean, default=False)
    purchase_price = db.Column(
        db.Integer
    )  # Dollars only, working with cents presents too many questions
    for_auction = db.Column(db.Boolean, default=False)
    auction_end = db.Column(db.DateTime)
    sold = db.Column(db.Boolean, default=False)

    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    bids = db.relationship("Bid", backref="listing", lazy="dynamic")

    def __repr__(self):
        image = True
        if self.image == "":
            image = False
        return f"<Listing: {self.id}, {self.timestamp}, {self.title}, {self.description}, {image}, {self.buyer_id}>"


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    value = db.Column(db.Numeric)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id"))

    def __repr__(self):
        return f"<Bid: {self.id}, {self.timestamp}, {self.value}, {self.user_id}, {self.listing_id}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
