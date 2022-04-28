from app.validators import RequiredIf
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, DateField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class LoginForm(FlaskForm):
    user_input = StringField("Username", validators=[DataRequired()])
    pswd_input = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
    submit = SubmitField("Create Listing")
