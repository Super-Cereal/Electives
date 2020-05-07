from flask import Flask, render_template
from blueprints import user_authenticate, tasks, groups, users

from data import db_session
# from data.model_groups import Group
# from data.model_tasks import Task
# from data.model_users import User


app = Flask(__name__)
app.config.from_object('config')
user_authenticate.login_manager.init_app(app)
db_session.global_init('./db/SQLiteBase.sqlite')

app.register_blueprint(user_authenticate.blueprint)
app.register_blueprint(groups.blueprint)
app.register_blueprint(tasks.blueprint)
app.register_blueprint(users.blueprint)
app.register_blueprint(tasks.blueprint)


# дописать html
@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


if __name__ == "__main__":
    if True:
        app.run()
    if False:
        session = db_session.create_session()
