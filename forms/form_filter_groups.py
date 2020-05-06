from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class FormFilterGroups(FlaskForm):
    filter_by = SelectField('Отобразить', choices=[(2, 'Все'), (1, 'Мои группы')], coerce=int)
    sort_by = SelectField('Отсортировать', choices=[(3, 'Без сортировки'), (2, 'По алфавиту'), (1, 'По колличеству участников')], coerce=int)
    submit = SubmitField('Показать')
