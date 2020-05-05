import time
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    email = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.String)
    last_time_in = sqlalchemy.Column(sqlalchemy.String,
                                     default=time.ctime)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    groups = sqlalchemy.orm.relation("Group",
                                     secondary="users_to_groups",
                                     backref="users")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
