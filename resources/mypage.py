from flask import make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models.child import ChildModel
from models.record import RecordModel


class EnrollChild(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('pin',
                         type=str,
                         required=True
                         )
    _parser.add_argument('name',
                         type=str,
                         required=True
                         )
    _parser.add_argument('gender',
                         type=str,
                         required=True
                         )
    _parser.add_argument('birth',
                         type=str,
                         required=True
                         )
    _parser.add_argument('doll',
                         type=str,
                         required=True
                         )

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        childs = ChildModel.find_all_by_user_id(user_id)

        resp = make_response({
            "response":[child.json() for child in childs]
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

class ChildRecordList(Resource):

    @jwt_required()
    def get(self,child_id):

        user_id = get_jwt_identity()

        records = RecordModel.find_all_by_child_id_with_user_id(child_id,user_id)

        resp = make_response({
            "response": records
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
