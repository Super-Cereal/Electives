from flask import Flask, redirect, abort
from flask_login import LoginManager, login_required, logout_user, login_user

from data import db_session
# from data.model_groups import Group
# from data.model_tasks import Task
from data.model_users import User

from forms.form_registration import FormRegistration
from form.form_login import FormLogin, current_user


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('./db/SQLiteBase.sqlite')


# не готова
@app.route('/', methods=['GET'])
def index():
    return '0'


# не готова
@app.route('/home/<int:user_id>', methods=['GET'])
def user_home(user_id):
    return '0'


# готова
@login_manager.user_loader
def user_load(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


# готова, написать html
# написать валидатор для проверки почты
@app.route('/register', methods=['GET', 'POST'])
def user_register():
    form = FormRegistration()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            type=form.type.data
        )
        user.set_password(form.password.data)
        session = db_session.create_session()
        session.add(user)
        session.commit()
        login_user(user)
        return redirect('/')
    else:
        return '0'


# готова, написать html
# написать валидаторы для проверки почты и пароля
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    form = FormLogin()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User.email).filter(User.email == form.email.data)
        login_user(user, remember=form.remember.data)
        return redirect('/')
    return '0'


# готова
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect('/')


# готова, написать html
@app.route('/edit_profile<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_edit_profile(user_id):
    if user_id != current_user.id:
        abort(403)
    form = FormRegistration()
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.age = form.age.data
        user.type = form.type.data
        session.commit()
        return redirect('/')
    else:
        form.name.data = user.name
        form.surname.data = user.surname
        form.email.data = user.email
        form.age.data = user.age
        form.type.data = user.type
        return '0'
    return '0'


# готова
@app.route('/del_profile<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_del_profile(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.comit()
    return redirect('/')


if __name__ == "__main__":
    if False:
        app.run()
    if True:
        session = db_session.create_session()
