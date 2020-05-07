import time
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


groups_to_tasks = sqlalchemy.Table('groups_to_tasks', SqlAlchemyBase.metadata,
                                   sqlalchemy.Column('groups', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id')),
                                   sqlalchemy.Column('tasks', sqlalchemy.Integer, sqlalchemy.ForeignKey('tasks.id')))


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.String, default=time.ctime)
    content = sqlalchemy.Column(sqlalchemy.String)
