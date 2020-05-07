from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, current_user

from data import db_session
from data.model_tasks import Task
from data.model_groups import Group

from forms.form_add_task import FormAddTask


blueprint = Blueprint('tasks', __name__,
                      template_folder='templates')


@blueprint.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
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
        session.commit()
        return redirect(f'/group/{group_id}')
    else:
        return render_template('form_add_task.html', form=form, group=group)


@blueprint.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    pass


@blueprint.route('/del_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def del_task(task_id):
    pass
