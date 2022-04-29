from app import db
from app import myobj
from app.forms import CreditCardForm, ListingForm, LoginForm
from app.models import Listing
from datetime import datetime
from flask import render_template, request, flash, redirect


@myobj.route("/")
def home():
    return render_template("homepage.html")


@myobj.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(form.user_input.data)
        return redirect("/")
    return render_template("login.html", form=form)


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

@myobj.route("/checkout", methods=["GET", "POST"])
def checkout():
    form = CreditCardForm()

    if form.validate_on_submit():
        expire_year = 2000 + form.expire_year.data
        today = datetime.today()
        if expire_year < today.year or (expire_year == today.year and form.expire_month.data < today.month):
            flash("Card is expired, submit another card")
        try:
            cc_number = int(form.number.data)
        except ValueError:
            flash("Entered an invalid credit card number.")
        try:
            cvv = int(form.cvv.data)
        except ValueError:
            flash("Entered an invalid CVV number.")
    return render_template(
        "checkout.html",
        title="Checkout",
        form=form,
    )
