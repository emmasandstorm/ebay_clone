from requests import session
from sqlalchemy import true
from app import db
from app import myobj
from app.forms import CreditCardForm, ListingForm, LoginForm, SignUpForm
from app.models import Listing, User
from app.utils import allowed_file
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, request, flash, redirect, session, url_for
import os
from werkzeug.utils import secure_filename


@myobj.route("/")
def home():
    return render_template("homepage.html")


@myobj.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()

        if user:
            if user.check_password(form.password.data):
                flash("Successful Login!!")
                login_user(user)

                return redirect("/")
            else:
                flash("Incorrect Password") 
        else:
            flash("Failed login")
    return render_template("login.html", form=form)

@myobj.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()

        if not user:
            u = User(username=username)
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            return redirect("/login")
        else:
            flash("You Already Have an Account!")

    return render_template("signup.html", form=form)


@myobj.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@myobj.route("/newlisting", methods=["GET", "POST"])
@login_required
def new_listing():
    form = ListingForm()

    if form.validate_on_submit():
        # Handle auction data
        if form.for_auction.data is True:
            if not form.auction_end.data:
                flash("End date is empty, validator not working")
                return redirect(request.referrer)

            if form.auction_end.data <= datetime.today().date():
                flash("Auction must end in the future.")
                return redirect(request.referrer)

        # Handle image upload
        if not form.image.data:
            flash("Please select an image")
            return redirect(request.referrer)

        file = form.image.data

        if file.filename == "":
            flash("Please select an image")
            return redirect(request.referrer)

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
                image=filename,
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
            listing=listing,
            description=listing.description,
            for_purchase=listing.for_purchase,
            price="${:,.2f}".format(price),
            filename=listing.image,
        )

    return redirect("/")


def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@myobj.route("/addcart", methods=["POST"])
@login_required
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
                session["Shoppingcart"] = MergeDicts(
                    session["Shoppingcart"], CartItems)
                return redirect("/cart")
        else:
            session["Shoppingcart"] = CartItems
            return redirect("/cart")

    return redirect("/")


@myobj.route("/cart", methods=["GET", "POST"])
@login_required
def display_cart():
    if "Shoppingcart" not in session:
        session["Shoppingcart"] = {}
    grandtotal = 0
    for key, item in session["Shoppingcart"].items():
        grandtotal += float(item["price"]) * float(item["quantity"])
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


@myobj.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = CreditCardForm()
    valid_card = False

    if form.validate_on_submit():
        expire_year = 2000 + form.expire_year.data
        today = datetime.today()
        if expire_year > today.year or (
            expire_year == today.year and form.expire_month.data > today.month
        ):
            valid_card = True
            try:
                cc_number = int(form.number.data)
            except ValueError:
                flash("Entered an invalid credit card number.")
                valid_card = False
            try:
                cvv = int(form.cvv.data)
            except ValueError:
                flash("Entered an invalid CVV number.")
                valid_card = False
        else:
            flash("Card is expired, submit another card")
        if valid_card is True:
            if "Shoppingcart" in session and session["Shoppingcart"]:
                try:
                    session.modified = True
                    for key, item in session["Shoppingcart"].items():
                        listing = Listing.query.filter_by(id=int(key)).first()
                        if listing is not None:
                            listing.sold = True
                            listing.buyer = current_user
                            db.session.commit()
                    session["Shoppingcart"].clear()
                except Exception as e:
                    print(e)
                flash("Listings bought!")
                return redirect("/cart")
            else:
                flash("Cart is empty, consider adding something to the cart.")
                return redirect("/cart")
    return render_template(
        "checkout.html",
        title="Checkout",
        form=form,
    )


@myobj.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="images/" + filename))
