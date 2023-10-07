from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class RegistrationUser(FlaskForm): #Форма, содержащая "Имя", "Фамилию", "Email", "Пароль" пользователя
    user_name = StringField('Имя пользователя', validators=[DataRequired()])
    user_surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_pass = PasswordField('Password', validators=[DataRequired(), Length(min=4)])