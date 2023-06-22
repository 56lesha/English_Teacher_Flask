from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError

from teacher.models import User


class CreateForm(FlaskForm):
    word = StringField(label="Enter Word:")
    translation = StringField(label="Enter English Translation: ")
    user_id = StringField(label="Enter user") # Убрать, когда сделаю авторизацию #Почему когда её убираю не работает?
    submit = SubmitField(label="Create new word ")


class UpdateForm(FlaskForm):
    id = IntegerField(label="Enter id of word you want to update") #Почему когда её убираю не работает?
    new_word = StringField(label="Enter new word: ")
    new_translation = StringField(label="Enter new translation: ")
    submit = SubmitField(label="Update word")


class RegistrationForm(FlaskForm):
    def validate_username(self, username_to_check): # если ф-ция начинается в validate, то он ищет переменную с названием, которая указана после нижнего подчёркивания
        username = User.query.filter_by(login=username_to_check.data).first()
        if username:
            raise ValidationError("Username already exists! Try to use another username")


    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Email already exists! Try to use another email")

    username = StringField(label="Enter username:", validators=[Length(min=2, max=30), DataRequired()])
    email_adress = StringField(label="Enter email:", validators=[Email(), DataRequired()])
    password_1 = PasswordField(label="Enter password:", validators=[Length(min=6), DataRequired()])
    password_2 = PasswordField(label="Confirm password:", validators=[EqualTo("password_1"), DataRequired()])
    submit = SubmitField(label="Create an account")



class LoginForm(FlaskForm):
    username=StringField(label="Enter username: ", validators=[DataRequired()])
    password = PasswordField(label ="Enter password: ", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")







