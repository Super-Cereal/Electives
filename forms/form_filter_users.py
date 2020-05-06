from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class FormFilterUsers(FlaskForm):
    filter_by = SelectField('Отобразить', choices=[(4, 'Всех'), (3, 'Учеников'), (2, 'Учителей'), (1, 'Администрацию')], coerce=int)
    sort_by = SelectField('Отсортировать', choices=[(3, 'Без сортировки'), (2, 'По алфавиту'), (1, 'По типу')], coerce=int)
    submit = SubmitField('Показать')
