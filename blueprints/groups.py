from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
import os

from data import db_session
from data.model_users import User
from data.model_groups import Group
from data.model_files import File


from forms.form_add_group import FormAddGroup
from forms.form_edit_group import FormEditGroup
from forms.form_filter_groups import FormFilterGroups


blueprint = Blueprint('groups', __name__,
                      template_folder='templates')


@blueprint.route('/groups', methods=["GET", "POST"])
def groups():
    session = db_session.create_session()
    form = FormFilterGroups()
    if form.validate_on_submit():
        if form.filter_by.data == 2:
            groups = session.query(Group).all()
        else:
            groups = current_user.groups
        if form.sort_by.data == 2:
            groups.sort(key=lambda x: x.name)
        elif form.sort_by.data == 1:
            groups.sort(key=lambda x: -x.users_num)
        return render_template('groups.html', groups=groups, bool_userbox=True, form=form)
    else:
        groups = session.query(Group).all()
        return render_template('groups.html', groups=groups, bool_userbox=True, form=form)


@blueprint.route('/group/<int:group_id>')
def group(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404)
    users = group.users
    tasks = group.tasks
    return render_template('group.html', group=group, users=users, tasks=tasks, bool_userbox=current_user.is_authenticated)


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
        user = session.query(User).get(form.leader_id.data)
        if not user:
            return render_template('form_add_group.html', form=form, message=f"Человека с id { form.leader_id.data } нет в системе")
        if user.type == 3:
            return render_template('form_add_group.html', form=form, message="Нельзя поставить в руководство ученика")
        group = Group(
            name=form.name.data,
            leader_id=form.leader_id.data,
            info=form.info.data,
            users_num=1
        )
        group.users.append(session.query(User).get(form.leader_id.data))
        session.add(group)
        session.commit()
        return redirect('/groups')
    else:
        if current_user.type == 2:
            form.leader_id.data = current_user.id
        return render_template('form_add_group.html', form=form)


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
        leader = session.query(User).get(form.leader_id.data)
        if not leader:
            return render_template('form_add_group.html', form=form, message=f"Человека с id {form.leader_id.data} нет в системе")
        if leader.type == 3:
            return render_template('form_add_group.html', form=form, message="Нельзя поставить в руководство ученика")
        if leader not in group.users:
            group.users.append(leader)
            group.users_num += 1
        group.name = form.name.data
        group.leader_id = form.leader_id.data
        group.info = form.info.data
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            path = f'/home/SuperCereal/status-false/static/downloads/group_{group.id}'
            if not os.path.exists(path):
                os.mkdir(path)
            if group.photo and os.path.exists(group.photo.path):
                os.remove(group.photo.path)
                session.delete(group.photo)
            form.photo.data.save(os.path.join(path, filename))
            photo = File(
                group_id=group.id,
                path=os.path.join(path, filename)
            )
            group.photo = photo
        session.commit()
        return redirect('/group/' + str(group_id))
    else:
        form.name.data = group.name
        form.info.data = group.info
        form.leader_id.data = group.leader_id
        return render_template('form_edit_group.html', form=form)


@blueprint.route('/del_group_photo/<int:group_id>')
def del_group_photo(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404)
    elif current_user.id != group.leader_id:
        abort(403)
    if group.photo:
        if os.path.exists(f'/home/SuperCereal/status-false/static/downloads/{group.id}'):
            os.remove(f'/home/SuperCereal/status-false/static/downloads/{group.id}')
        session.delete(group.photo)
        session.commit()
    return redirect(f'/group/{group_id}')


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
    if os.path.exists(f'/home/SuperCereal/status-false/static/downloads/group_{group.id}'):
        for root, dirs, files in os.walk(f'/home/SuperCereal/status-false/static/downloads/group_{group.id}', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    session.delete(group)
    session.commit()
    return redirect('/groups')


@blueprint.route('/join_group/<int:group_id>')
@login_required
def join_group(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404)
    if current_user not in group.users:
        group.users.append(session.query(User).get(current_user.id))
        group.users_num += 1
    session.commit()
    return redirect('/group/' + str(group_id))


@blueprint.route('/leave_group/<int:group_id>')
@login_required
def leave_group(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404)
    if current_user.id == group.leader_id:
        abort(403)
    if current_user in group.users:
        group.users.remove(session.query(User).get(current_user.id))
        group.users_num -= 1
    session.commit()
    return redirect('/group/' + str(group_id))
