from app import db
from app import myobj
from app.forms import ListingForm, LoginForm
from app.models import Listing
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
        l = Listing(
            title=form.title.data,
            description=form.description.data,
            for_purchase=form.for_purchase.data,
            purchase_price=form.purchase_price.data,
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
            listing_title=listing.title,
            description=listing.description,
            for_purchase=listing.for_purchase,
            price="${:,.2f}".format(price),
        )
    return redirect("/")
