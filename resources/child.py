from flask import make_response, request
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models.child import ChildModel
from models.record import RecordModel
from models.doll import DollModel


class Child(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        childs = ChildModel.find_all_by_user_id(user_id)

        return {
            "response": [child.json() for child in childs]
        }



class ChildInfo(Resource):
    @jwt_required()
    def delete(self,child_id):
        user_id = get_jwt_identity()

        childs = ChildModel.find_all_by_user_id(user_id)

        for child in childs:
            if child.id == child_id:
                doll = DollModel.find_by_child_id(child_id)
                doll.child_id = None
                doll.save_to_db()

                child.delete_from_db()

                return {
                    "message": "성공적으로 제거했습니다."
                }

        return {
            "message": "제거할 수 없습니다."
        }, 400

class ChildRecordList(Resource):

    @jwt_required()
    def get(self,child_id):

        user_id = get_jwt_identity()

        records = RecordModel.find_all_by_child_id_with_user_id(child_id,user_id)

        return {
            "response": [record.json() for record in records]
        }
