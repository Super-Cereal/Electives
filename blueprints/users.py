from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, current_user

from forms.form_edit_user import FormEditUser
from forms.form_filter_users import FormFilterUsers

from data import db_session
from data.model_users import User


blueprint = Blueprint('users', __name__,
                      template_folder='templates')


# написать html
@blueprint.route('/home/<int:user_id>')
def home(user_id):
    return render_template('base.html')

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
    groups = user.groups
    return render_template('user.html', user=user, groups=groups)


# готова
@blueprint.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    if user_id != current_user.id:
        abort(403)
    form = FormEditUser()
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
@blueprint.route('/del_profile<int:user_id>')
@login_required
def del_profile(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.comit()
    return redirect('/')
