from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, current_user

from data import db_session
from data.model_users import User

from blueprints.macros.delete_downloads_structure import delete_downloads_structure
from blueprints.macros.delete_file_if_exists import delete_file_if_exists
from blueprints.macros.save_file import save_file

from forms.form_edit_user import FormEditUser
from forms.form_filter_users import FormFilterUsers


blueprint = Blueprint('users', __name__,
                      template_folder='templates')


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


@blueprint.route('/user/<int:user_id>')
def user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    groups = user.groups
    return render_template('user.html', user=user, groups=groups, bool_userbox=(current_user.is_authenticated and (current_user.id == user_id or current_user.type <= 1)))


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
        if form.photo.data:
            delete_file_if_exists(file=user.photo, session=session)
            user.photo = save_file(data=form.photo.data, path=f'static/downloads/user_{user_id}')
        session.commit()
        return redirect(f'/user/{user_id}')
    else:
        form.name.data = user.name
        form.surname.data = user.surname
        form.age.data = user.age
        form.email.data = user.email
        return render_template('form_edit_user.html', form=form)


@blueprint.route('/del_user_photo/<int:user_id>', methods=['GET', 'POST'])
@login_required
def del_user_photo(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    elif current_user.id != user.id:
        abort(403)
    delete_file_if_exists(file=user.photo, session=session)
    return redirect(f'/user/{user_id}')


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
            delete_downloads_structure(path=f'static/downloads/group_{ group.id }')
            session.delete(group)
    delete_downloads_structure(path=f'static/downloads/user_{ user.id }')
    session.delete(user)
    session.commit()
    return redirect('/')
