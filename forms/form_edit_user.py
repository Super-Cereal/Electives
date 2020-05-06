from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FormEditUser(FlaskForm):
    name = StringField('Ваше имя :', validators=[DataRequired(message='Поле должно быть заполнено')])
    surname = StringField('Ваша фамилия :', validators=[DataRequired(message='Поле должно быть заполнено')])
    age = IntegerField('Ваш возраст :', validators=[DataRequired(message='Поле должно быть заполнено'),
                                                    NumberRange(min=6, max=115, message='Возраст должен быть в промежутке от 6 лет до 115')])
    submit = SubmitField('Отправить')
