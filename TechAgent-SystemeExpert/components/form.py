from tkinter.tix import Select
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, IntegerRangeField
from wtforms.validators import DataRequired
from wtforms.validators import NoneOf


class Todo(FlaskForm):
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Submit todo')


class Order(FlaskForm):
    marque = SelectField("marque", validators=[NoneOf("def")])
    # ram = SelectField("ram", validators=[NoneOf(["Ram"])])
    # stockage = SelectField("stockage", validators=[NoneOf(["Stockage"])])
    # price = IntegerRangeField("price")
