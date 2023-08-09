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

class Counselor(Resource):

    COUNSELOR_DATA_KEY_CATEGORY = "category"
    COUNSELOR_DATA_KEY_LOCATION = "location"
    COUNSELOR_MEMBERSHIP_TYPE_VERIFIED = "정회원"
    """
    TODO:
        여기는 ~~하는곳
    """
    _parser = reqparse.RequestParser()
    _parser.add_argument(COUNSELOR_DATA_KEY_CATEGORY,
                         type=str,
                         required=False,
                         action='append'
                         )
    _parser.add_argument(COUNSELOR_DATA_KEY_LOCATION,
                         type=str,
                         required=False,
                         action='append'
                         )


    @staticmethod
    def filter_by_category(category):

        if category != None:
            categories = CategoryModel.find_all_by_list_name(category)
            categories_id = [category.id for category in categories]

            counselors_id = [mid_category.counselor_id for mid_category in
                             MidCategoryModel.find_by_id_with_list_category_id(categories_id)]
            counselors_id.count(10)
            counselors_id = set(counselors_id)

            return [CounselorModel.find_by_id(counselor) for counselor in counselors_id]
        else:
            return CounselorModel.find_all()


    @staticmethod
    def filter_by_location(counselors,location):
        return [counselor for counselor in counselors if counselor.address_range in location]

    def get(self):
        data = Counselor._parser.parse_args()

        counselors_by_category = Counselor.filter_by_category(data[Counselor.COUNSELOR_DATA_KEY_CATEGORY])

        if data[Counselor.COUNSELOR_DATA_KEY_LOCATION] != None:
            counselors = Counselor.filter_by_location(counselors_by_category,data[Counselor.COUNSELOR_DATA_KEY_LOCATION])
        else :
            counselors = counselors_by_category
        return {
            "response": [counselor.json() for counselor in counselors if counselor.state == Counselor.COUNSELOR_MEMBERSHIP_TYPE_VERIFIED]
        }

class CounselorInfo(Resource):

    def get(self,counselor_id):

        counselor = CounselorModel.find_by_id(counselor_id)
        careers = CareerModel.find_by_counselor_id(counselor_id)
        licenses = LicenseModel.find_by_counselor_id(counselor_id)
        available_times = AvailableTimeModel.find_by_counselor_id(counselor_id)

        times = dict()

        for time in available_times:
            times[time.day] = time.json()

        return {
            "profile": counselor.json(),
            "intro_title": counselor.intro_title,
            "intro_content": counselor.intro_content,
            "career": [career.json() for career in careers],
            "license": [license.json() for license in licenses],
            "time": times
        }

class CounselorTimeAvailability(Resource):

    def get(self,counselor_id):

        available_times = AvailableTimeModel.find_by_counselor_id(counselor_id)

        times = dict()

        for time in available_times:
            times[time.day] = time.json()

        return {
            "interval": available_times[0].interval,
            "time": times
        }