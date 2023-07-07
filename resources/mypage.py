from flask import make_response
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models.child import ChildModel
from models.record import RecordModel
from models.doll import DollModel
import datetime


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
                         type=lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"),
                         required=True
                         )
    _parser.add_argument('doll',
                         type=str,
                         required=True
                         )
    _parser.add_argument('thumbnail',
                         type=str,
                         required=False
                         )

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        data = EnrollChild._parser.parse_args()

        child = ChildModel(
            user_id,
            data['name'],
            data['birth'],
            data['gender'],
            data['thumbnail'],
            datetime.datetime.now()
        )
        child.save_to_db()

        doll = DollModel.find_by_pin(data['pin'])
        doll.child_id = child.id
        doll.name = data['name']
        doll.save_to_db()

        resp = make_response({
            "message":"Child has been created!"
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

class DollComCheck(Resource):

    """
    TODO:
        소켓통신으로 인형과 연결되었는지 확인하는 로직이 필요함!
    """
    @jwt_required()
    def get(self,child_id):

        user_id = get_jwt_identity()

        records = RecordModel.find_all_by_child_id_with_user_id(child_id,user_id)

        resp = make_response({
            "response": records
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
