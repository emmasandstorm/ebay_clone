from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


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
            NumberRange(
                min=0, max=1000000, message="Price must be between 0 and 1000000."
            )
        ],
    )
    submit = SubmitField("Create Listing")
