from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True)
parser.add_argument('type', required=True)
parser.add_argument('email', required=True)
