from wsgiref.validate import validator
from app.validators import RequiredIf
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (
    BooleanField,
    IntegerField,
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Register")


class ListingForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    for_purchase = BooleanField("Available for Instant Purchase?")
    purchase_price = IntegerField(
        "Purchase Price",
        validators=[
            Optional(),
            NumberRange(
                min=0, max=1000000, message="Price must be between 0 and 1000000."
            ),
        ],
    )
    for_auction = BooleanField("Accept Bids")
    auction_end = DateField("Until", validators=[RequiredIf(for_auction=True)])
    image = FileField("Image", validators=[FileRequired()])
    submit = SubmitField("Create Listing")


class AuctionForm(FlaskForm):
    price = IntegerField("Price", validators=[DataRequired(), NumberRange(
        min=0, max=1000000, message="Price must be between 0 and 1000000.")])
    submit = SubmitField("Place Your Bid")


# trying it just as an HTML form
'''class AddtoCart(FlaskForm):
    # for now, quantity is too much
    quantity = IntegerField(
        "quantity",
        validators=[NumberRange(min=1, max=None, message=None)]
    )
    submit = SubmitField("Add to Cart")'''


class CreditCardForm(FlaskForm):
    number = StringField("Credit Card Number", validators=[DataRequired(), Length(
        min=16, max=16, message="Please enter a 16 digit credit card number."), ],)
    name = StringField("Name on Card", validators=[DataRequired()])
    expire_month = SelectField("MM", choices=["01", "02", "03", "04", "05", "06",
                               "07", "08", "09", "10", "11", "12"], coerce=int, validators=[DataRequired()])
    expire_year = SelectField("YY", choices=[
                              "22", "23", "24", "25", "26", "27"], coerce=int, validators=[DataRequired()],)
    cvv = StringField("CVV", validators=[DataRequired(), Length(
        min=3, max=3, message="Please enter the 3 digit code on the back of the card.")],)
    submit = SubmitField("Confirm Purchase")
