from flask_restful import Resource, reqparse
from models import CounselorModel,IndexPageModel,ReservationModel,UserModel

class GetCounselors(Resource):

    def get(self):
        counselors = CounselorModel.find_all()

        counselor_list = [
            {
                "profile":{
                    "id":counselor.id,
                    "thumbnail":counselor.profile,
                    "name":counselor.user_subname,
                    "breif":counselor.brief_desc,
                },
                "times":{
                    "open":counselor.available_begin,
                    "close":counselor.available_end
                }
            }
            for counselor in counselors
        ]

        return {"counselors":counselor_list}

class GetPageInfo(Resource):
    def get(self,id):
        page = IndexPageModel.find_by_counselor_id(id)

        return page.json()


class MakeReservation(Resource):
    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('day',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _user_parser.add_argument('begin',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _user_parser.add_argument('end',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _user_parser.add_argument('user_id',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _user_parser.add_argument('counselor_id',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _user_parser.add_argument('content',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )

    def post(self):
        data = MakeReservation._user_parser.parse_args()

        reservation = ReservationModel(
            day=data['day'],
            begin=data['begin'],
            end=data['end'],
            user_id=data['user_id'],
            counselor_id=data['counselor_id'],
            content=data['content']
        )
        reservation.save_to_db()

        return {"message":"Reservation has just been made."},200


class GetUserReservation(Resource):
    def get(self,id):
        reservations = ReservationModel.find_by_user_id(id)
        if not reservations == None:
            reservations_list=[
                {
                    "status":reservation.status,
                    "counselor":CounselorModel.find_by_id(reservation.counselor_id).json(),
                    "detail":{
                        "day":reservation.day,
                        "begin":reservation.begin,
                        "end":reservation.end,

                        "content":[content.strip() for content in reservation.content.split("\n") if((content.strip()))]
                    }
                }
                for reservation in reservations
            ]
        else :
            reservations_list = []
        return {"reservations":reservations_list}

class GetCounselorReservation(Resource):
    def get(self,id):
        reservations = ReservationModel.find_by_counselor_id(id)
        if not reservations == None:
            reservations_list=[
                {
                    "status": reservation.status,
                    "user":UserModel.find_by_id(reservation.user_id).json(),
                    "detail":{
                        "day":reservation.day,
                        "begin":reservation.begin,
                        "end":reservation.end,

                        "content":[content.strip() for content in reservation.content.split("\n") if((content.strip()))]
                    }
                }
                for reservation in reservations
            ]
        else :
            reservations_list = []
        return {"reservations":reservations_list}

class AcceptReservation(Resource):
    def post(self,id):
        reservation = ReservationModel.find_by_id(id)
        reservation.status = "ACCEPTED"
        reservation.save_to_db()
        return {"message":"ok"},200

class RejectReservation(Resource):
    def post(self,id):
        reservation = ReservationModel.find_by_id(id)
        reservation.status = "REJECTED"
        reservation.save_to_db()
        return {"message": "ok"}, 200

class CancleReservation(Resource):
    def delete(self,id):
        reservation = ReservationModel.find_by_id(id)
        reservation.delete_from_db()
        return {"message": "ok"}, 200