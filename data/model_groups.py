import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property

from .db_session import SqlAlchemyBase
from .db_session import create_session
from data.model_users import User


users_to_groups_table = sqlalchemy.Table('users_to_groups', SqlAlchemyBase.metadata,
                                         sqlalchemy.Column('users', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
                                         sqlalchemy.Column('groups', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id')))


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    leader_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey('users.id'))
    info = sqlalchemy.Column(sqlalchemy.String)
    users_num = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    photo = sqlalchemy.orm.relation("File", uselist=False)
    tasks = sqlalchemy.orm.relation("Task", backref="group")

    @hybrid_property
    def leader(self):
        session = create_session()
        leader = session.query(User).get(self.leader_id)
        return leader
