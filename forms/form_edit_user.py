from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField
from wtforms.validators import DataRequired, NumberRange, Email, ValidationError

from werkzeug.utils import secure_filename


class FormEditUser(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(message='Поле должно быть заполнено')])
    surname = StringField('Ваша фамилия', validators=[DataRequired(message='Поле должно быть заполнено')])
    age = IntegerField('Ваш возраст', validators=[DataRequired(message='Поле должно быть заполнено'),
                                                  NumberRange(min=6, max=115, message='Возраст должен быть в промежутке от 6 лет до 115')])
    email = StringField('Ваша контактная почта', validators=[DataRequired(message='Поле должно быть заполнено'), Email(message='Неккоректно задана почта')])
    photo = FileField('Изменить изображение на профиле')
    submit = SubmitField('Отправить')

    def validate_photo(self, field):
        if field.data:
            filename = secure_filename(field.data.filename)
            if filename.rsplit('.', 1)[1] not in ('png', 'jpeg', 'jpg'):
                raise ValidationError("Недопустимое расширение для фото, используйте .png или .jpeg(.jpg)")
