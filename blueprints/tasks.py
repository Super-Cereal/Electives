from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
import os

from data import db_session
from data.model_tasks import Task
from data.model_groups import Group
from data.model_files import File

from forms.form_add_task import FormAddTask


blueprint = Blueprint('tasks', __name__,
                      template_folder='templates')


@blueprint.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    session = db_session.create_session()
    groups_n_tasks = [(group, group.tasks) for group in current_user.groups]
    return render_template('tasks.html', groups_n_tasks=groups_n_tasks)


@blueprint.route('/add_task/<int:group_id>', methods=['GET', 'POST'])
@login_required
def add_task(group_id):
    session = db_session.create_session()
    form = FormAddTask()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404)
    elif group.leader_id != current_user.id:
        abort(403)
    if form.validate_on_submit():
        task = Task(
            name=form.name.data,
            content=form.content.data
        )
        session.add(task)
        group.tasks.append(task)
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            path = f'static/downloads/group_{group.id}'
            if not os.path.exists(path):
                os.mkdir(path)
            if task.file and os.path.exists(task.file.path):
                os.remove(task.file.path)
                session.delete(task.file)
            form.file.data.save(os.path.join(path, filename))
            file = File(
                task_id=task.id,
                path=os.path.join(path, filename)
            )
            task.file = file
        session.commit()
        return redirect(f'/group/{group_id}')
    else:
        return render_template('form_add_task.html', form=form, group=group)


@blueprint.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if not task:
        abort(404)
    if task.group.leader_id != current_user.id:
        abort(403)
    form = FormAddTask()
    if form.validate_on_submit():
        task.name = form.name.data
        task.content = form.content.data

        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            path = f'static/downloads/group_{task.group.leader_id}'
            if not os.path.exists(path):
                os.mkdir(path)
            if task.file and os.path.exists(task.file.path):
                os.remove(task.file.path)
                session.delete(task.file)
            form.file.data.save(os.path.join(path, filename))
            file = File(
                task_id=task.id,
                path=os.path.join(path, filename)
            )
            task.file = file
        session.commit()
        return redirect(f'/group/{task.group.leader_id}')
    else:
        form.name.data = task.name
        form.content.data = task.content
        return render_template('form_edit_task.html', form=form, task=task)


@blueprint.route('/del_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def del_task(task_id):
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    if not task:
        abort(404)
    if task.group.leader_id != current_user.id and current_user.id >= 2:
        abort(403)
    if task.file and os.path.exists(task.file.path):
        os.remove(task.file.path)
    group_id = task.group.leader_id
    session.delete(task)
    session.commit()
    return redirect(f'/group/{group_id}')
