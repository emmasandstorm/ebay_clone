from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    #cart = db.relationship('Cart', backref='User', lazy ='dynamic')

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
    # relationship with cart
    #cart = db.relationship('Cart', backref='Listing', lazy ='subquery')
    #purchased = db.Column(db.Boolean, db.ForeignKey('cart.purchase_status'))

    def __repr__(self):
        return f"<Listing: {self.id}, {self.timestamp}, {self.title}, {self.description}, {self.user_id}>"
'''
cart_listings = db.Table('Listings',
    db.Column('listing_title', db.String(128), db.ForeignKey('Listing.title')),
    db.Column('listing_price', db.Integer, db.ForeignKey('listing.purchase_price')),
    db.Column('listing_description', db.String(256), db.ForeignKey('listing.description'))
    )

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cart_listings = db.relationship('Listing', secondary=cart_listings, lazy='subquery',
        backref=db.backref('carts', lazy=True))
    #title = db.Column(db.String(128), db.ForeignKey('listing.title'))
    #description = db.Column(db.String(256), db.ForeignKey('listing.description'))
    #price = db.Column(db.Integer, db.ForeignKey('listing.purchase_price'))
    purchase_status = db.Column(db.Boolean, default = False)
    #If a listing is purchased, then the listing gets updated
    purchased = db.relationship('Listing', backref='Cart', lazy='dynamic')'''



"""class Cart():
    id
    user_id (column)
    listings (relationship)
    It occurs to me that for this to work we will actually need to update the listing to have a cart value
    When someone clicks add to cart, this listing itself gets updated. 
    That cart value could be unique, making it so adding something to your cart gives you exclusive rights to buy it
    In the wild that might be a problem, but for this application I think that's the best move
    Alternatively the "listings" section could be a string that we concatenate with ids when the user presses buttons
    I think that approach is a little hackier/messier, but may be worthwhile
    There may be a third way to do this that I'm not seeing, but """
