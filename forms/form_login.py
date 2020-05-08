from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


class FormLogin(FlaskForm):
    email = StringField('Ваша почта', validators=[DataRequired(message='Поле должно быть заполнено'), Email(message='Неккоректно задана почта')])
    password = PasswordField('Ваш пароль', validators=[DataRequired(message='Поле должно быть заполнено')])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Отправить')
