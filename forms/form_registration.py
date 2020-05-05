from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange, Length


class FormRegistration(FlaskForm):
    name = StringField('Ваше имя :', validators=[DataRequired(message='Поле должно быть заполнено')])
    surname = StringField('Ваша фамилия :', validators=[DataRequired(message='Поле должно быть заполнено')])
    age = IntegerField('Ваш возраст :', validators=[DataRequired(message='Поле должно быть заполнено'),
                                                    NumberRange(min=6, max=115, message='Возраст должен быть в промежутке от 6 лет до 115')])
    type = SelectField('Вы :', choices=[(3, 'Ученик'), (2, 'Учитель'), (1, 'Администрация')], coerce=int)
    email = StringField('Ваша контактная почта :', validators=[DataRequired(message='Поле должно быть заполнено'), Email(message='Неккоректно задана почта')])
    password = PasswordField('Ваш пароль :', validators=[DataRequired(message='Поле должно быть заполнено'),
                                                         Length(min=5, message='Пароль должен быть длиннее 5 символов, это ваша безопасность!')])
    password_again = PasswordField('Повторите пароль :', [DataRequired(EqualTo('password', message='Пароли должны совпадать'))])
    submit = SubmitField('')
