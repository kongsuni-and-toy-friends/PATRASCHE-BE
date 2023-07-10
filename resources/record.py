from flask import make_response
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models.chat import ChatModel
from models.record import RecordModel

class Chat(Resource):

    @jwt_required()
    def get(self,record_id):
        user_id = get_jwt_identity()

        chats = ChatModel.find_all_by_user_id_with_record_id(user_id,record_id)

        return {
            "response": [chat.json() for chat in chats]
        }

# class ChildRecordList(Resource):
#
#     @jwt_required()
#     def get(self,child_id):
#
#         user_id = get_jwt_identity()
#
#         childs = ChildModel.find_all_by_user_id(user_id)
#
#         is_vaild = False
#         for child in childs:
#             if child.id == child_id:
#                 is_vaild = True
#                 break
#
#         if is_vaild :
#             records = [record.json() for record in RecordModel.find_all_by_child_id(child_id)]
#         else :
#             records = []
#
#         resp = make_response({
#             "response": records
#         })
#         resp.headers['Access-Control-Allow-Origin'] = '*'
#         return resp
