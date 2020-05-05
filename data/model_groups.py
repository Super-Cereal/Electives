import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


users_to_groups_association_table = sqlalchemy.Table('users_to_groups', SqlAlchemyBase.metadata,
                                                     sqlalchemy.Column('users', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
                                                     sqlalchemy.Column('groups', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id')))


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    teacher = sqlalchemy.Column(sqlalchemy.Integer)
    tasks = sqlalchemy.orm.relation("Task",
                                    secondary="groups_to_tasks",
                                    backref="groups")
