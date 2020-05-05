from flask import Flask, render_template
from flask_login import LoginManager

from blueprints import user_authenticate

from data import db_session
# from data.model_groups import Group
# from data.model_tasks import Task
from data.model_users import User


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('./db/SQLiteBase.sqlite')

app.register_blueprint(user_authenticate.blueprint)


@login_manager.user_loader
def user_load(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


# дописать html
@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


# не готова
@app.route('/home/<int:user_id>', methods=['GET'])
def user_home(user_id):
    return '0'


if __name__ == "__main__":
    if True:
        app.run()
    if False:
        session = db_session.create_session()
