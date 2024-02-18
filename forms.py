from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, AnyOf


class RegistrationForm(FlaskForm):
    firstname = StringField('Имя', validators=[DataRequired()])
    lastname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, message='Минимальная длина пароля 8 символов'),
    ])
