from flask import make_response, request
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models.chat import ChatModel
from models.category import CategoryModel,MidCategoryModel
from models.career import CareerModel
from models.license import LicenseModel
from models.availabletime import AvailableTimeModel
from models.record import RecordModel
from models.counselor import CounselorModel
from models.pre_reservation import PreReservationModel
from models.post_reservation import PostReservationModel
from models.user import UserModel
from models.child import ChildModel
import datetime

class V2PreReservation(Resource):

    @jwt_required()
    def get(self):

        counselor_id = get_jwt_identity()

        reservations = PreReservationModel.find_by_counselor_id(counselor_id)

        resp = make_response({
            "response":[reserve.json() for reserve in reservations]
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


class V2PreReservationInfo(Resource):

    @jwt_required()
    def get(self,reservation_id):

        counselor_id = get_jwt_identity()

        data = PreReservationModel.find_by_counselor_id_with_id(counselor_id,reservation_id)

        response = {}
        user = UserModel.find_by_id(data.user_id)
        child = ChildModel.find_by_id(data.child_id)
        response['name'] = child.name
        response['phone'] = user.phone
        response['email'] = user.email
        response['birth'] = datetime.datetime.strftime(child.birth,"%Y-%m-%d")
        response['start'] = datetime.datetime.strftime(data.start_time,"%H:%M:%S")
        response['date'] = datetime.datetime.strftime(data.date,"%Y-%m-%d")
        response['problem'] = data.problem

        resp = make_response({
            "response":response
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

class PostReservation(Resource):

    @jwt_required()
    def get(self,counselor_id):

        user_id = get_jwt_identity()
        reservations = PostReservationModel.find_by_user_id(user_id)

        resp = make_response({
            "response":[reserve.json() for reserve in reservations]
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
