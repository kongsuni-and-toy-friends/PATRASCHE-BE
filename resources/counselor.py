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

class Counselor(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('category',
                         type=str,
                         required=False,
                         action='append'
                         )
    _parser.add_argument('location',
                         type=str,
                         required=False,
                         action='append'
                         )
    def get(self):
        data = Counselor._parser.parse_args()

        if 'category' in data.keys():
            categories = CategoryModel.find_all_by_list_name(data['category'])
            categories_id = [cate.id for cate in categories]

            counselors_id = [mcate.counselor_id for mcate in MidCategoryModel.find_by_id_with_list_category_id(categories_id)]
            counselors_id = set(counselors_id)

            counselors = [CounselorModel.find_by_id(counselor) for counselor in counselors_id]
        else :
            counselors = CounselorModel.find_all()

        if 'location' in data.keys():
            counselors = [counselor for counselor in counselors if counselor.address_range in data['location']]

        resp = make_response({
            "response":[counselor.json() for counselor in counselors]
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

class CounselorInfo(Resource):

    def get(self,counselor_id):

        counselor = CounselorModel.find_by_id(counselor_id)
        careers = CareerModel.find_by_counselor_id(counselor_id)
        licenses = LicenseModel.find_by_counselor_id(counselor_id)
        times = AvailableTimeModel.find_by_counselor_id(counselor_id)

        resp = make_response({
            "profile": counselor.json(),
            "intro_title": counselor.intro_title,
            "intro_content": counselor.intro_content,
            "career":[career.json() for career in careers],
            "license":[license.json() for license in licenses],
            "time":[time.json() for time in times]
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

class CounselorTime(Resource):

    def get(self,counselor_id):

        counselor = CounselorModel.find_by_id(counselor_id)
        times = AvailableTimeModel.find_by_counselor_id(counselor_id)

        resp = make_response({
            "interval":times[0].interval,
            "time":[time.json() for time in times]
        })
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp