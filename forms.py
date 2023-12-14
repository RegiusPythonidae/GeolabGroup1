from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, RadioField, DateField, SelectField
from wtforms.validators import DataRequired, length, equal_to


class AddProductForm(FlaskForm):
    name = StringField("პროდუქტის სახელი", validators=[DataRequired()])
    price = IntegerField("ფასი", validators=[DataRequired()])
    img = FileField("ატვირთეთ სურათი", validators=[FileRequired()])

    submit = SubmitField("დამატება")


class RegisterForm(FlaskForm):
    username = StringField("ჩაწერეთ იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("ჩაწერეთ პაროლი",
                             validators=[
                                 DataRequired(),
                                 length(min=8, max=64)
                             ])
    repeat_password = PasswordField("გაიმეორეთ პაროლი",
                                    validators=[
                                        DataRequired(),
                                        equal_to("password", message="პაროლები არ ემთხვევა")
                                    ])
    gender = RadioField("სქესი", choices=["კაცი", "ქალი"], validators=[DataRequired()])
    birthday = DateField("დაბადების თარიღი", validators=[DataRequired()])
    country = SelectField("ქვეყანა", choices=["Georgia", "United States", "Germany"], validators=[DataRequired()])

    register = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField("ჩაწერეთ იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("ჩაწერეთ პაროლი", validators=[DataRequired()])

    login = SubmitField("ავტორიზაცია")