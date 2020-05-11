from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length


class FormAddTask(FlaskForm):
    name = StringField('Название', validators=[DataRequired(message="Поле должно быть заполнено")])
    content = TextAreaField('Текст задания', validators=[Length(min=4, message='Текст задания должен содержать хотя бы 4 символа')])
    file = FileField('Прикрепить файл')
    submit = SubmitField('Отправить')
