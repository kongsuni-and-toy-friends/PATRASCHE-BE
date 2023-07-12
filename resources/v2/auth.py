import datetime

from flask import make_response, request
from flask_restx import Resource, reqparse
from hmac import compare_digest
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)
import json
import requests
from models import UserModel
from models import CounselorModel
from models import LicenseModel
from models import CareerModel
from models import DegreeModel

class CounselorKakao(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('code',
                         type=str,
                         required=True,
                         help="This field cannot be blank."
                         )

    token_server = "https://kauth.kakao.com/oauth/token"
    restapi_key = "cfe89bc232781d31c8bc26d93dd746fe"
    redirect_url = "http://localhost:5173/kakao"
    userme_url = "https://kapi.kakao.com/v2/user/me"
    client_secret = "mgN9eDJYxpbHxdtcrh1M2o4qYRzDJKkS"

    def post(self):

        code_data = CounselorKakao._parser.parse_args()
        code = code_data["code"]

        response = requests.post(
            url = CounselorKakao.token_server,
            headers={
                'Content-Type':"application/x-www-form-urlencoded",
                'Cache-Control':"no-cache"
            },
            data = {
                "grant_type": "authorization_code",
                "client_id": CounselorKakao.restapi_key,
                "client_secret": CounselorKakao.client_secret,
                "redirect_uri": CounselorKakao.redirect_url,
                "code": code,
            }
        )

        try:
            access_token = json.loads(((response.text).encode('utf-8')))['access_token']
        except :

            return {
                "message": "Invaild token"
            }

        response = requests.get(
            url = CounselorKakao.userme_url,
            headers={
                'Authorization' : f"Bearer ${access_token}"
            }
        )
        user_data = json.loads(((response.text).encode('utf-8')))['kakao_account']
        name = user_data['name']
        email = user_data["email"]
        birth = f"{user_data['birthyear']}-{user_data['birthday'][:2]}-{user_data['birthday'][2:]}"

        phone = "0" + user_data["phone_number"].split(" ")[1]
        gender = user_data['gender']

        counselor = CounselorModel.find_by_email(email)

        if counselor:
            access_token = create_access_token(identity=counselor.id, fresh=True)
            refresh_token = create_refresh_token(counselor.id)

            return {
                "registered": True,
                "access": access_token,
                "refresh": refresh_token,
                "state": counselor.state,
                "name":counselor.name
            }
        else :
            return {
                "registered": False,
                "name":name,
                "email":email,
                "gender":gender,
                "birth":birth,
                "phone":phone,
                "provider":"kakao"
            }

class CounselorRegister(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('email',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _parser.add_argument('pw',
                              type=str,
                              required=False,
                              help="This field cannot be blank."
                              )
    _parser.add_argument('name',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _parser.add_argument('birth',
                            type=lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"),
                            required=True,
                            help="This field cannot be blank."
                            )
    _parser.add_argument('gender',
                         type=str,
                         required=True,
                         help="This field cannot be blank."
                         )
    _parser.add_argument('phone',
                         type=str,
                         required=True,
                         help="This field cannot be blank."
                         )
    _parser.add_argument('address',
                         type=str,
                         required=True,
                         help="This field cannot be blank."
                         )
    _parser.add_argument('address_range',
                         type=str,
                         required=True,
                         help="This field cannot be blank."
                         )
    _parser.add_argument('provider',
                         type=str,
                         required=False,
                         help="This field cannot be blank."
                         )
    _parser.add_argument('thumbnail',
                         type=str,
                         required=False,
                         help="This field cannot be blank."
                         )

    def post(self):
        data = CounselorRegister._parser.parse_args()

        counselor = CounselorModel(
            data['name'],
            data['phone'],
            data['email'],
            data['gender'],
            data['address'],
            data['address_range'],
            data['birth'],
            datetime.datetime.now()
        )
        if data["pw"] != "":
            counselor.password = data['pw']
        if data["provider"] != "":
            counselor.provider = data["provider"]
        else :
            counselor.provider = "common"
        if data["thumbnail"] != "":
            counselor.thumbnail = data["thumbnail"]

        counselor.state = "준회원"
        counselor.save_to_db()

        access_token = create_access_token(identity=counselor.id, fresh=True)
        refresh_token = create_refresh_token(counselor.id)

        return {
            "message": "Counselor created successfully.",
            "access": access_token,
            "refresh": refresh_token,
            "state": counselor.state
        }

class CounselorDupCheck(Resource):
    def get(self):
        email = request.args.get("email")

        if CounselorModel.find_by_email(email):

            return {
                "result": False,
                "message": "이미 가입한 이메일입니다."
            }
        else :
            return {
                "result": True
            }

#

class CounselorLogin(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('email',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )
    _parser.add_argument('pw',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )

    def post(self):
        data = CounselorLogin._parser.parse_args()
        counselor = CounselorModel.find_by_email(data['email'])

        # this is what the `authenticate()` function did in security.py
        if counselor:
            if compare_digest(counselor.password, data['pw']):
                # identity= is what the identity() function did in security.py—now stored in the JWT
                access_token = create_access_token(identity=counselor.id, fresh=True)
                refresh_token = create_refresh_token(counselor.id)


                return {
                    "access": access_token,
                    "refresh": refresh_token,
                    "state": counselor.state
                }

        return {
            "message": "Invalid Credentials!"
        }

class CounselorProfile(Resource):
    _parser = reqparse.RequestParser()
    _parser.add_argument('email',
                              type=str,
                              required=False
                              )
    _parser.add_argument('phone',
                              type=str,
                              required=False
                              )
    _parser.add_argument('address',
                         type=str,
                         required=False
                         )
    _parser.add_argument('address_range',
                         type=str,
                         required=False
                         )
    _parser.add_argument('address_range',
                         type=str,
                         required=False
                         )
    _parser.add_argument('thumbnail',
                         type=str,
                         required=False
                         )
    _parser.add_argument('title',
                         type=str,
                         required=False
                         )
    _parser.add_argument('content',
                         type=str,
                         required=False
                         )

    @jwt_required()
    def put(self):

        counselor_id = get_jwt_identity()

        data = CounselorLogin._parser.parse_args()
        counselor = CounselorModel.find_by_id(counselor_id)

        if 'email' in data.keys():
            counselor.email = data['email']
        if 'phone' in data.keys():
            counselor.phone = data['phone']
        if 'address' in data.keys():
            counselor.address = data['address']
        if 'address_range' in data.keys():
            counselor.address_range = data['address_range']
        if 'thumbnail' in data.keys():
            counselor.thumbnail = data['thumbnail']
        if 'title' in data.keys():
            counselor.intro_title = data['title']
        if 'content' in data.keys():
            counselor.intro_content = data['content']

        counselor.save_to_db()

        return {
            "message": "Changes has been taken!"
        }


class CounselorApprove(Resource):
    # _parser = reqparse.RequestParser()
    # _parser.add_argument('degree',
    #                           type=list,
    #                           required=True,
    #                             location="json"
    #                           )
    # _parser.add_argument('career',
    #                           type=list,
    #                           required=True,
    #                      location="json"
    #                           )
    # _parser.add_argument('license',
    #                      type=list,
    #                      required=True,
    #                      location="json"
    #                      )

    @jwt_required()
    def post(self):
        data = request.get_json()
        print(data)
        counselor_id = get_jwt_identity()

        counselor = CounselorModel.find_by_id(counselor_id)

        degrees = data['degree']
        careers = data['career']
        licenses = data['license']

        for data in degrees:
            if data['graduation']:
                grad = datetime.datetime.strptime(data['graduation'],"%Y-%m-%d")
            else:
                grad = None
            degree = DegreeModel(
                data['degree'],
                data['name'],
                data['subject'],
                data['major'],
                datetime.datetime.strptime(data['entrance'],"%Y-%m-%d"),
                grad,
                data['type'],
                data['cert'],
                counselor.id
            )
            degree.save_to_db()

        for data in careers:
            if data['end']:
                end = datetime.datetime.strptime(data['end'],"%Y-%m-%d")
            else:
                end = None
            career = CareerModel(
                data['name'],
                datetime.datetime.strptime(data['start'],"%Y-%m-%d"),
                data['type'],
                data['role'],
                data['cert'],
                counselor.id,
                end
            )
            career.save_to_db()

        for data in licenses:
            career = LicenseModel(
                data['name'],
                datetime.datetime.strptime(data['date'],"%Y-%m-%d"),
                data['cert'],
                data['organization'],
                counselor.id
            )
            career.save_to_db()

        return {
            "message": "Request has been taken!"
        }

#   class User(Resource):
#     """
#     This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
#     sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
#     """
#     def get(self):
#         user_id = 1
#
#         user = UserModel.find_by_id(user_id)
#         if not user:
#             user = CounselorModel.find_by_id(user_id)
#             if not user :
#                 return {'message': 'User Not Found'}, 404
#         return user.json(), 200
#
#     def delete(self):
#         user_id = 1
#
#         user = UserModel.find_by_user_id(user_id)
#         if not user:
#             return {'message': 'User Not Found'}, 404
#         user.delete_from_db()
#         return {'message': 'User deleted.'}, 200