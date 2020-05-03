from flask import Flask, redirect
from flask_login import LoginManager, login_required, logout_user

from data import db_session


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)


# не готова
@app.route('/', methods=['GET'])
def index():
    return '0'


# не готова
@app.route('/home/<int:user_id>', methods=['GET'])
def user_home(user_id):
    return '0'


# не готова
@login_manager.user_loader
def user_load(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


# не готова
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    form = ''
    if form.validate_on_submit():
        pass
    return '0'


# не готова
@app.route('/register', methods=['GET', 'POST'])
def user_register():
    form = ''
    if form.validate_on_submit():
        pass
    return '0'


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect('/')


# не готова
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def user_edit_profile():
    form = ''
    if form.validate_on_submit():
        pass
    return '0'


# не готова
@app.route('/del_profile', methods=['GET', 'POST'])
@login_required
def user_del_profile():
    return '0'


if __name__ == "__main__":
    app.run()
