from app import db
from app import myobj
from app.forms import ListingForm, LoginForm
from app.models import Listing
from app.utils import allowed_file
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename

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
        #Handle auction data
        if form.for_auction.data is True:
            if not form.auction_end.data:
                flash("End date is empty, validator not working")
                return redirect(request.url)

            if form.auction_end.data <= datetime.utcnow().date():
                flash("Auction must end in the future.")
                return redirect(request.url)

        #Handle image upload
        if not form.image.data:
            flash("Please select an image")
            return redirect(request.url)

        file = form.image.data

        if file.filename == "":
            flash("Please select an image")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if not os.path.exists(myobj.config["UPLOAD_FOLDER"]):
                os.makedirs(myobj.config["UPLOAD_FOLDER"])

            file.save(os.path.join(myobj.config["UPLOAD_FOLDER"], filename))

            l = Listing(
                title=form.title.data,
                description=form.description.data,
                for_purchase=form.for_purchase.data,
                purchase_price=form.purchase_price.data,
                for_auction=form.for_auction.data,
                auction_end=form.auction_end.data,
                image=filename
            )
            db.session.add(l)
            db.session.commit()

            return render_template(
                "newlisting.html",
                title="New Listing",
                form=form,
                filename=l.image,
            )
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
            filename=listing.image,
        )
    return redirect("/")


@myobj.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="images/" + filename))