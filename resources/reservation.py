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
import datetime

class PreReservation(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        reservations = PreReservationModel.find_by_user_id(user_id)

        return {
            "response": [reserve.json() for reserve in reservations]
        }

class PostReservation(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()
        reservations = PostReservationModel.find_by_user_id(user_id)

        return {
            "response": [reserve.json() for reserve in reservations]
        }

class MakeReservation(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('date',
                         type=lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"),
                         required=True
                         )
    _parser.add_argument('start',
                         type=lambda x: datetime.datetime.strptime(x,"%H:%M:%S"),
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


        return {
            "message": "예약이 완료되었습니다."
        }