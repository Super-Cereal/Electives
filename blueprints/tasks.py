from flask import Blueprint, redirect, abort, render_template
from flask_login import login_required, current_user

from data import db_session
from data.model_users import User
from data.model_tasks import Task



blueprint = Blueprint('tasks', __name__,
                      template_folder='templates')


@blueprint.route('/tasks', methods=['GET'])
def tasks():
    session = db_session.create_session()
    tasks = session.query(Task).all()


@blueprint.route('/add_task', methods=['GET', 'POST'])
def add_task():
    pass


@blueprint.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    pass


@blueprint.route('/del_task/<int:task_id>', methods=['GET', 'POST'])
def del_task(task_id):
    pass
