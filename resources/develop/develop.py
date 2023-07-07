import datetime

from flask import make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import *

class MakeMock(Resource):

    def get(self,record_id):

        user = UserModel.find_by_useremail("test@gmail.com")

        if user :
            resp = make_response({
                "message": "Already made mock"
            })
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

        user = UserModel(
            "테스트유저",
            "test@gmail.com",
            "male",
            datetime.datetime.strptime("1998-01-01","%Y-%m-%d"),
            datetime.datetime.now(),
            "010-1234-5678",
            "서울 강남구",
            "1q2w3e4r"
        )

        user.save_to_db()

        child = ChildModel(
            user.id,
            "김철수",
            datetime.datetime.strptime("2023-01-01","%Y-%m-%d"),
        )

        chats = ChatModel.find_all_by_user_id_with_record_id(user_id,record_id)

        resp = make_response({
            "response":[chat.json() for chat in chats]
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

