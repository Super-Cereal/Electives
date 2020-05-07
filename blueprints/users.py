from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, current_user

from forms.form_edit_user import FormEditUser
from forms.form_filter_users import FormFilterUsers

from data import db_session
from data.model_users import User


blueprint = Blueprint('users', __name__,
                      template_folder='templates')


# готова
@blueprint.route('/users/', methods=['GET', 'POST'])
def users():
    session = db_session.create_session()
    form = FormFilterUsers()
    if form.validate_on_submit():
        if form.filter_by.data == 4:
            users = session.query(User).all()
        else:
            users = session.query(User).filter(User.type == form.filter_by.data).all()
        if form.sort_by.data == 2:
            users.sort(key=lambda x: (x.name, x.surname))
        elif form.sort_by.data == 1:
            users.sort(key=lambda x: x.type)
        return render_template('users.html', users=users, bool_userbox=True, form=form)
    else:
        users = session.query(User).all()
        return render_template('users.html', users=users, bool_userbox=True, form=form)


# готова
@blueprint.route('/user/<int:user_id>')
def user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    groups = user.groups
    return render_template('user.html', user=user, groups=groups, bool_userbox=(current_user.id == user_id or current_user.type <= 1))


# готова
@blueprint.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if user_id != current_user.id:
        abort(403)
    form = FormEditUser()
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.email = form.email.data
        session.commit()
        return redirect('/')
    else:
        form.name.data = user.name
        form.surname.data = user.surname
        form.age.data = user.age
        form.email.data = user.email
        return render_template('form_edit_user.html', form=form)


# готова
@blueprint.route('/del_user/<int:user_id>')
@login_required
def del_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    if current_user.type >= 2 and current_user.id != user_id:
        abort(403)
    for group in user.groups:
        group.users_num -= 1
        if group.leader_id == user_id:
            session.delete(group)
    session.delete(user)
    session.commit()
    return redirect('/')
