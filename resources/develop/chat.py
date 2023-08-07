import datetime

from flask import make_response
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import *

class RecvMsg(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('message',
                         type=str,
                         required=True,
                         help="This field cannot be blank."
                         )
    def post(self):
        data = RecvMsg._parser.parse_args()
        print(data)
        return "SUCCESS", 200

