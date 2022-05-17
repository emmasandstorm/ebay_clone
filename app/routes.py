from sqlalchemy import true
from app import db
from app import myobj
from app import search
from app.forms import AuctionForm, CreditCardForm, ListingForm, LoginForm, SignUpForm, UserBioForm
from app.models import Bid, Listing, User
from app.utils import allowed_file, MergeDicts
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, request, flash, redirect, session
import os
from werkzeug.utils import secure_filename

# homepage
@myobj.route("/")
def home():
    items = Listing.query.all()
    return render_template("homepage.html", items = items)

# login page
@myobj.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()

        # successful login
        if user:
            if user.check_password(form.password.data):
                flash("Successful Login!!")
                login_user(user)

                return redirect("/")
            else:
                # if text entered doesn't match database
                flash("Failed login")
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
            login_user(u)
            return redirect("/")
        else:
            flash("Username taken, please select another one.")

    return render_template("signup.html", form=form)


@myobj.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = UserBioForm()

    if form.validate_on_submit():

        user_bio = form.user_bio.data

        current_user.user_profile = user_bio
        db.session.commit()
        return redirect(f"/profile/{current_user.username}")

    return render_template("editprofile.html", username=current_user.username, form=form)

# profile page displays username, bio, and collection of valid users
@myobj.route("/profile/<username>/", methods=["GET", "POST"])
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        if user == current_user:
            return render_template( "profile.html", username=user.username, bio=user.user_profile, items=user.collection, show_buttons=True)
        return render_template(
            "profile.html", username=user.username, bio=user.user_profile, items=user.collection)
    else:
        flash("No such user")
        return redirect("/")

# logout page is only a placeholder for the logout function, then redirects to login page
@myobj.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/login")

@myobj.route("/delete/<username>/", methods=["GET", "POST"])
@login_required
def delete(username):
    if username == current_user.username:
        db.session.delete(current_user)
        db.session.commit()
        flash("Your account has been removed!")
        return redirect("/")
    else:
        flash("You can only delete your own account!")
        return redirect("/")

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

        # Handle image validation and upload
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

            # All data valid, image stored. Create and store new listing.
            l = Listing(
                title=form.title.data,
                description=form.description.data,
                seller_id=current_user.id,
                image=filename,
                for_purchase=form.for_purchase.data,
                purchase_price=form.purchase_price.data,
                for_auction=form.for_auction.data,
                auction_end=form.auction_end.data,
            )
            db.session.add(l)
            db.session.commit()

            return redirect("/listing/" + str(l.id))
    return render_template("newlisting.html", title="New Listing", form=form)

@myobj.route("/search")
def searchresult():
    searchword = request.args.get('q')
    items = Listing.query.msearch(searchword, fields = ['title', 'description', 'purchase_price'], limit=10)
    return render_template('search.html', items=items, q=searchword)

@myobj.route("/listing/<listing_id>", methods=["GET", "POST"])
def display_listing(listing_id):
    listing = Listing.query.filter_by(id=listing_id).first()
    if listing is not None:

        # Handle instant purchase
        price = listing.purchase_price
        if price is None:
            price = 0

        # Handle bidding for auctionable items
        if listing.for_auction is True:

            highest_bid = listing.bids.order_by(Bid.value.desc()).first()
            if highest_bid is None:
                highest_bid = Bid(value=0)

            # Auction is ongoing, accept bids
            if datetime.now() < listing.auction_end:
                form = AuctionForm()

                if form.validate_on_submit():
                    if form.price.data <= highest_bid.value:
                        flash(
                            f"${form.price.data}.00 is not larger than the highest bid.")
                    else:
                        b = Bid(
                            value=form.price.data,
                            bidder=current_user,
                            listing_id=listing_id,
                        )
                        db.session.add(b)
                        db.session.commit()
                        highest_bid = b

                return render_template(
                    "listing.html",
                    title=f"Listing {listing_id}",
                    listing=listing,
                    description=listing.description,
                    for_purchase=listing.for_purchase,
                    price=price,
                    filename=listing.image,
                    accepts_bids=listing.for_auction,
                    highest_bid="${:,.2f}".format(highest_bid.value),
                    form=form,
                )

            # Auction has ended, do not accept bids
            else:
                # Someone won the auction, only they should see checkout
                if highest_bid.bidder is not None:
                    if current_user == highest_bid.bidder:
                        return render_template(
                            "listing.html",
                            title=f"Listing {listing_id}",
                            listing=listing,
                            description=listing.description,
                            for_purchase=listing.for_purchase,
                            price=highest_bid.value,
                            filename=listing.image,
                            accepts_bids=listing.for_auction,
                            winner=True,
                            checkout=True
                        )
                    # Someone won, but not the current user
                    else:
                        return render_template(
                            "listing.html",
                            title=f"Listing {listing_id}",
                            listing=listing,
                            description=listing.description,
                            for_purchase=listing.for_purchase,
                            price=highest_bid.value,
                            filename=listing.image,
                            accepts_bids=listing.for_auction,
                            winner=True,
                            checkout=False
                        )
        # Either no auction or auction ended with no bids
        return render_template(
            "listing.html",
            title=f"Listing {listing_id}",
            listing=listing,
            description=listing.description,
            for_purchase=listing.for_purchase,
            price=price,
            filename=listing.image,
        )
    return redirect("/")

# add to cart functionality
@myobj.route("/addcart", methods=["POST"])
@login_required
def AddCart():
    # creates a dictionary with all the important information about the listing, grabbed from the Listing database
    # the dictionary is attributed to the user session, so it saves while the user is logged in.
    listing_id = request.form.get("listing_id")
    quantity = int(request.form.get("quantity"))
    price = int(float(request.form.get("price")))
    product = Listing.query.filter_by(id=listing_id).first()
    if listing_id and quantity and request.method == "POST":
        CartItems = {
            listing_id: {
                "name": product.title,
                "price": price,
                "description": product.description,
                "quantity": quantity,
                "image": product.image,
            }
        }
        # if there is already something in the cart
        if "Shoppingcart" in session:
            print(session["Shoppingcart"])
            # trying to add the same item twice
            if listing_id in session["Shoppingcart"]:
                flash("This product is already in your cart")
                return redirect(request.referrer)
            else:
                session["Shoppingcart"] = MergeDicts(
                    session["Shoppingcart"], CartItems)
                return redirect("/cart")
        # if the cart is empty
        else:
            session["Shoppingcart"] = CartItems
            return redirect("/cart")

    return redirect("/")

# display cart page
@myobj.route("/cart", methods=["GET", "POST"])
@login_required
def display_cart():
    # when there is nothing in the shopping cart, an empty cart is shown
    if "Shoppingcart" not in session:
        session["Shoppingcart"] = {}
    grandtotal = 0
    # table in cart.html pulls all values accordingly and the grandtotal is calculated as well
    for key, item in session["Shoppingcart"].items():
        grandtotal += int(float(item["price"])) * int(float(item["quantity"]))
    return render_template(
        "cart.html", total=session["Shoppingcart"], grandtotal=grandtotal
    )

# removing an item functionality
@myobj.route("/removecartitem/<int:id>")
def removeitem(id):
    if "Shoppingcart" not in session and len(session["Shoppingcart"]) <= 0:
        return redirect("/")
    # if the remove button is clicked, the shopping cart dictionary will be edited
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

    # Validate credit card information (but don't check if it's a real card)
    if form.validate_on_submit():
        expire_year = 2000 + form.expire_year.data
        today = datetime.today()
        if expire_year > today.year or (
            expire_year == today.year and form.expire_month.data >= today.month
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

        # Card validation was successful, purchase the contents of the cart
        if valid_card is True:
            if "Shoppingcart" in session and session["Shoppingcart"]:
                try:
                    session.modified = True
                    for key, item in session["Shoppingcart"].items():
                        listing = Listing.query.filter_by(id=int(key)).first()
                        if listing is not None:
                            if listing.sold == False:
                                listing.sold = True
                                listing.buyer = current_user
                                db.session.commit()
                            else:
                                flash(
                                    f"{listing.title} was purchased by another user while in your cart. Sorry! Gotta be quick on FreEbay!")
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
