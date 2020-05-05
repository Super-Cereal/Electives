import time
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, null=False)
    start_date = sqlalchemy.Column(sqlalchemy.String, default=time.ctime)
    duration = sqlalchemy.Column(sqlalchemy.String)
