from requests import session
from sqlalchemy import true
from app import db
from app import myobj
from app.forms import ListingForm, LoginForm
from app.models import Listing, User
from datetime import datetime
from flask_login import login_user, logout_user, login_required
from flask import render_template, request, flash, redirect, session


@myobj.route("/")
def home():
    return render_template("homepage.html")


@myobj.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        print("hi")
        if user:
            if user.check_password(form.password.data):
                flash("Successful Login!!")
                login_user(user)
                return redirect("/")
            else:
                flash("Incorrect Password")
        else:
            flash("Failed login")
            print("hello")

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
            listing=listing,
            description=listing.description,
            for_purchase=listing.for_purchase,
            price="${:,.2f}".format(price),
        )

    return redirect("/")


def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@myobj.route("/addcart", methods=["POST"])
def AddCart():
    listing_id = request.form.get("listing_id")
    quantity = int(request.form.get("quantity"))
    product = Listing.query.filter_by(id=listing_id).first()
    if listing_id and quantity and request.method == "POST":
        CartItems = {
            listing_id: {
                "name": product.title,
                "price": product.purchase_price,
                "description": product.description,
                "quantity": quantity,
            }
        }
        if "Shoppingcart" in session:
            print(session["Shoppingcart"])
            if listing_id in session["Shoppingcart"]:
                flash("This product is already in your cart")
                return redirect(request.referrer)
            else:
                session["Shoppingcart"] = MergeDicts(session["Shoppingcart"], CartItems)
                return redirect("/cart")
        else:
            session["Shoppingcart"] = CartItems
            return redirect("/cart")

    return redirect("/")


@myobj.route("/cart", methods=["GET", "POST"])
def display_cart():
    if "Shoppingcart" not in session:
        return redirect("/")
    grandtotal = 0
    for key, item in session["Shoppingcart"].items():
        grandtotal += float(item["price"])
    return render_template(
        "cart.html", total=session["Shoppingcart"], grandtotal=grandtotal
    )


@myobj.route("/removecartitem/<int:id>")
def removeitem(id):
    if "Shoppingcart" not in session and len(session["Shoppingcart"]) <= 0:
        return redirect("/")
    try:
        session.modified = True
        for key, item in session["Shoppingcart"].items():
            if int(key) == id:
                session["Shoppingcart"].pop(key, None)
                return redirect("/cart")
        pass
    except Exception as e:
        print(e)
        return redirect("/cart")
