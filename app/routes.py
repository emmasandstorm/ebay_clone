from sqlalchemy import true
from app import db
from app import myobj
from app.forms import ListingForm, LoginForm
from app.models import Listing, User
from datetime import datetime
from flask_login import login_user, logout_user, login_required
from flask import render_template, request, flash, redirect


@myobj.route("/")
def home():
    return render_template("homepage.html")


@myobj.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        print('hi')
        if user:
            if user.check_password(form.password.data):
                flash("Successful Login!!")
                login_user(user)
                return redirect("/")
            else:
                flash("Incorrect Password")
        else:
            flash("Failed login")
            print('hello')
        
    return render_template("login.html", form=form)



@myobj.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@myobj.route("/newlisting", methods=["GET", "POST"])
def new_listing():
    form = ListingForm()

    if form.validate_on_submit():
        if form.for_auction.data is True:
            if form.auction_end.data is None:
                flash("End date is empty, validator not working")
                return redirect(request.url)
            if form.auction_end.data <= datetime.utcnow().date():
                flash("Auction must end in the future.")
                return redirect(request.url)

        l = Listing(
            title=form.title.data,
            description=form.description.data,
            for_purchase=form.for_purchase.data,
            purchase_price=form.purchase_price.data,
            for_auction=form.for_auction.data,
            auction_end=form.auction_end.data,
        )
        db.session.add(l)
        db.session.commit()
    return render_template("newlisting.html", title="New Listing", form=form)


@myobj.route("/listing/<listing_id>")
def display_listing(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is not None:
        price = listing.purchase_price
        if price is None:
            price = 0
        return render_template(
            "listing.html",
            title=f"Listing {listing_id}",
            listing=listing.title,
            description=listing.description,
            for_purchase=listing.for_purchase,
            price="${:,.2f}".format(price),
        )
    return redirect("/")

@myobj.route("/cart")
def display_cart():
    return render_template("cart.html")