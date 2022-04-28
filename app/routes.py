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
def upload_form():
    form = ListingForm()

    if form.validate_on_submit():
        l = Listing(title=form.title.data, description=form.description.data)
        print(l)
    return render_template("newlisting.html", title="New Listing", form=form)
