from flask import Blueprint, redirect, abort, render_template, request
from flask_login import login_required, current_user

from data import db_session
from data.model_users import User
from data.model_groups import Group

from forms.form_add_group import FormAddGroup
from forms.form_edit_group import FormEditGroup


blueprint = Blueprint('groups', __name__,
                      template_folder='templates')


# работает
@blueprint.route('/groups', methods=["GET", "POST"])
def groups():
    session = db_session.create_session()
    if request.method == 'POST' and current_user.is_authenticated:
        groups = current_user.groups
    else:
        groups = session.query(Group).all()
    return render_template('groups.html', groups=groups, bool_userbox=current_user.is_authenticated)


# работает
@blueprint.route('/group/<int:group_id>')
def group(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    users = group.users
    return render_template('group.html', group=group, users=users, bool_userbox=current_user.is_authenticated)


# работает
@blueprint.route('/add_group', methods=["GET", "POST"])
@login_required
def add_group():
    if current_user.type == 3:
        abort(403)
    session = db_session.create_session()
    form = FormAddGroup()
    if form.validate_on_submit():
        if current_user.type == 2 and form.leader_id.data != current_user.id:
            return render_template('form_add_group.html', form=form, message="Как учитель, вы можете создать факультатив только под своим руководством, ваш id - " + str(current_user.id))
        if session.query(User).get(form.leader_id.data).type == 3:
            return render_template('form_add_group.html', form=form, message="Нельзя поставить в руководство ученика")
        group = Group(
            name=form.name.data,
            leader_id=form.leader_id.data,
            info=form.info.data,
            users_num=1
        )
        group.users.append(session.query(User).get(current_user.id))
        session.add(group)
        session.commit()
        return redirect('/groups')
    else:
        if current_user.type == 2:
            form.leader_id.data = current_user.id
        return render_template('form_add_group.html', form=form)


# работает
@blueprint.route('/edit_group/<int:group_id>', methods=["GET", "POST"])
@login_required
def edit_group(group_id):
    if current_user.type == 3:
        abort(403)
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404)
    elif current_user.type == 2 and not group.leader_id == current_user.id:
        abort(403)
    form = FormEditGroup()
    if form.validate_on_submit():
        if current_user.type == 2 and form.leader_id.data != current_user.id:
            return render_template('form_add_group.html', form=form, message="Как учитель, вы можете создать факультатив только под своим руководством, ваш id - " + str(current_user.id))
        if session.query(User).get(form.leader_id.data).type == 3:
            return render_template('form_add_group.html', form=form, message="Нельзя поставить в руководство ученика")
        group.name = form.name.data
        group.leader_id = form.leader_id.data
        group.info = form.info.data
        session.commit()
        return redirect('/group/' + str(group_id))
    else:
        form.name.data = group.name
        form.info.data = group.info
        form.leader_id.data = group.leader_id
        return render_template('form_add_group.html', form=form)


# работает
@blueprint.route('/del_group/<int:group_id>')
@login_required
def del_group(group_id):
    if current_user.type == 3:
        abort(403)
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404)
    elif current_user.type == 2 and not group.leader_id == current_user.id:
        abort(403)
    session.delete(group)
    session.commit()
    return redirect('/groups')
