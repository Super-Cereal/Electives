from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
import os

from forms.form_edit_user import FormEditUser
from forms.form_filter_users import FormFilterUsers

from data import db_session
from data.model_users import User
from data.model_files import File


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
            filename = secure_filename(form.photo.data.filename)
            path = f'/home/SuperCereal/status-false/static/downloads/user_{user.id}'
            if not os.path.exists(path):
                os.mkdir(path)
            if user.photo and os.path.exists(user.photo.path):
                os.remove(user.photo.path)
                session.delete(user.photo)
            form.photo.data.save(os.path.join(path, filename))
            photo = File(
                user_id=user.id,
                path=os.path.join(path, filename)
            )
            user.photo = photo
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
    if user.photo:
        if os.path.exists(user.photo.path):
            os.remove(user.photo.path)
        session.delete(user.photo)
        session.commit()
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
            if os.path.exists(f'/home/SuperCereal/status-false/static/downloads/group_{group.id}'):
                for root, dirs, files in os.walk(f'/home/SuperCereal/status-false/static/downloads/group_{group.id}', topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
            session.delete(group)
    if user.photo and os.path.exists(f'/home/SuperCereal/status-false/static/downloads/user_{user_id}'):
        for root, dirs, files in os.walk(f'/home/SuperCereal/status-false/static/downloads/user_{user_id}', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    session.delete(user)
    session.commit()
    return redirect('/')
