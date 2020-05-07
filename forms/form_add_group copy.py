from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


class FormAddGroup(FlaskForm):
    name = StringField('Название', validators=[DataRequired(message="Поле должно быть заполнено")])
    leader_id = IntegerField("id руководителя", validators=[DataRequired(message="Поле должно быть заполнено")])
    info = TextAreaField("Информация о факультативе")
    submit = SubmitField('Отправить')
