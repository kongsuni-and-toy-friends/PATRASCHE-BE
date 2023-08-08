from flask import make_response
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models.child import ChildModel
from models.record import RecordModel


class Child(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        childs = ChildModel.find_all_by_user_id(user_id)
        for child in childs:
            print(child.name)
            print(child.id)

        return {
            "response": [child.json() for child in childs]
        }

class ChildRecordList(Resource):

    @jwt_required()
    def get(self,child_id):

        user_id = get_jwt_identity()

        records = RecordModel.find_all_by_child_id_with_user_id(child_id,user_id)

        return {
            "response": [record.json() for record in records]
        }
