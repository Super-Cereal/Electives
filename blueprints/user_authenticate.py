from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, logout_user, login_user, current_user

from data import db_session
from data.model_users import User
from forms.form_registration import FormRegistration
from forms.form_login import FormLogin
from forms.form_edit import FormEdit


blueprint = Blueprint('user_authenticate', __name__,
                      template_folder='templates')


# готова
@blueprint.route('/registration', methods=['GET', 'POST'])
def user_register():
    form = FormRegistration()
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
def user_login():
    form = FormLogin()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if not user or not user.check_password(form.password.data):
            return render_template('form_login.html', form=form, message="Неправильный логин или пароль")
        login_user(user, remember=form.remember.data)
        return redirect('/')
    return render_template('form_login.html', form=form)


# готова
@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect('/')


# готова
@blueprint.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_edit_profile(user_id):
    if user_id != current_user.id:
        abort(403)
    form = FormEdit()
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        session.commit()
        return redirect('/')
    else:
        form.name.data = user.name
        form.surname.data = user.surname
        form.age.data = user.age
        return render_template('form_edit.html', form=form)


# готова
@blueprint.route('/del_profile<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_del_profile(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.comit()
    return redirect('/')
