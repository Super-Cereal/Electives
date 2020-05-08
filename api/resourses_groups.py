from data.db_session import create_session
from data.model_groups import Group

from flask_restful import abort, Resource
from flask import jsonify


class GroupResourse(Resource):
    def get(self, group_id):
        session = create_session()
        group = session.query(Group).get(group_id)
        if not group:
            abort(404, message=f'Group {group_id} not found')
        return jsonify(
            {
                'groups': [group.to_dict(only=['id', 'name', 'info', 'leader_id', 'users_num'])]
            }
        )


class GroupListResourse(Resource):
    def get(self):
        session = create_session()
        groups = session.query(Group).all()
        return jsonify(
            {
                'groups': [group.to_dict(only=['id', 'name', 'info', 'leader_id', 'users_num']) for group in groups]
            }
        )
