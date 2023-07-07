from flask import make_response, request
from flask_restful import Resource, reqparse
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

class PreReservation(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        reservations = PreReservationModel.find_by_user_id(user_id)

        resp = make_response({
            "response":[reserve.json() for reserve in reservations]
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

class MakeReservation(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('date',
                         type=str,
                         required=True
                         )
    _parser.add_argument('start',
                         type=str,
                         required=True
                         )
    _parser.add_argument('problem',
                         type=str,
                         required=True
                         )
    _parser.add_argument('child_id',
                         type=str,
                         required=True
                         )

    @jwt_required()
    def post(self,counselor_id):

        user_id = get_jwt_identity()

        data = MakeReservation._parser.parse_args()

        reservation = PreReservationModel(
            data['date'],
            data['problem'],
            data['start'],
            "대기",
            counselor_id,
            user_id,
            data['child_id']
        )

        reservation.save_to_db()

        resp = make_response({
            "message":"예약이 완료되었습니다."
        })
        resp.status_code = 201
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp