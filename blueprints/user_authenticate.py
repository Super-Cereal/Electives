from flask import Blueprint, redirect, render_template
from flask_login import login_required, logout_user, login_user, LoginManager
import time

from data import db_session
from data.model_users import User
from forms.form_add_user import FormAddUser
from forms.form_login import FormLogin


blueprint = Blueprint('user_authenticate', __name__,
                      template_folder='templates')
login_manager = LoginManager()


# готова
@login_manager.user_loader
def user_load(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


# готова
@blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = FormAddUser()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            type=form.type.data
        )
        user.set_password(form.password.data)
        session = db_session.create_session()
        session.add(user)
        session.commit()
        login_user(user)
        return redirect('/')
    else:
        return render_template('form_registration.html', form=form)


# готова
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if not user or not user.check_password(form.password.data):
            return render_template('form_login.html', form=form, message="Неправильный логин или пароль")
        user.last_time_in = time.ctime()
        session.commit()
        login_user(user, remember=form.remember.data)
        return redirect('/')
    return render_template('form_login.html', form=form)


# готова
@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')
