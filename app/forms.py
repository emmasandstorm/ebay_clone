from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    user_input = StringField("Username", validators=[DataRequired()])
    pswd_input = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
