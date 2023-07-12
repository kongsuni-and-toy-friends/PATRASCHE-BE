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

class UserKakao(Resource):
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

        code_data = UserKakao._parser.parse_args()
        code = code_data["code"]

        response = requests.post(
            url = UserKakao.token_server,
            headers={
                'Content-Type':"application/x-www-form-urlencoded",
                'Cache-Control':"no-cache"
            },
            data = {
                "grant_type": "authorization_code",
                "client_id": UserKakao.restapi_key,
                "client_secret": UserKakao.client_secret,
                "redirect_uri": UserKakao.redirect_url,
                "code": code,
            }
        )

        try:
            access_token = json.loads(((response.text).encode('utf-8')))['access_token']
        except :
            print("No token")
            return {
                "message": "Invaild token"
            }, 400

        response = requests.get(
            url = UserKakao.userme_url,
            headers={
                'Authorization' : f"Bearer ${access_token}"
            }
        )
        user_data = json.loads(((response.text).encode('utf-8')))['kakao_account']
        #print(user_data)
        # user_profile = user_data['profile']

        name = user_data['name']
        email = user_data["email"]
        birth = f"{user_data['birthyear']}-{user_data['birthday'][:2]}-{user_data['birthday'][2:]}"

        phone = "0" + user_data["phone_number"].split(" ")[1]
        gender = user_data['gender']
        user = UserModel.find_by_useremail(email)

        if user:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                "registered":True,
                "access": access_token,
                "refresh": refresh_token,
                "name":user.name
            }
        else :
            return{
                "registered": False,
                "name":name,
                "email":email,
                "gender":gender,
                "birth":birth,
                "phone":phone,
                "provider":"kakao"
            }


class UserRegister(Resource):
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
        data = UserRegister._parser.parse_args()

        user = UserModel.find_by_useremail(data['email'])

        if user:
            return {
                "message": f"Email {data['email']} had been taken!"
            }, 409

        user = UserModel(
            data['name'],
            data['email'],
            data['gender'],
            data['birth'],
            datetime.datetime.now(),
            data['phone'],
            data['address']
        )
        if data["pw"] != "":
            user.password = data['pw']
        if data["provider"] != "":
            user.provider = data["provider"]
        else :
            user.provider = "common"
        if data["thumbnail"] != "":
            user.thumbnail = data["thumbnail"]
        user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {
            "message": "User created successfully.",
            "access": access_token,
            "refresh": refresh_token,
        }, 201

class UserDupCheck(Resource):
    def get(self):
        email = request.args.get("email")

        if UserModel.find_by_useremail(email):

            return {
                "result": False,
                "message": "이미 가입한 이메일입니다."
            }, 409
        else :
            return {
                "result": True
            }, 200

class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """
    def get(self):
        user_id = 1

        user = UserModel.find_by_id(user_id)
        if not user:
            user = CounselorModel.find_by_id(user_id)
            if not user :
                return {'message': 'User Not Found'}, 404
        return user.json(), 200

    def delete(self):
        user_id = 1

        user = UserModel.find_by_user_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

class UserLogin(Resource):
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
        data = UserLogin._parser.parse_args()
        user = UserModel.find_by_useremail(data['email'])

        # this is what the `authenticate()` function did in security.py
        if user :
            if compare_digest(user.password, data['pw']):
                # identity= is what the identity() function did in security.py—now stored in the JWT
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)

                return {
                    "access": access_token,
                    "refresh": refresh_token,
                    "name": user.name
                }, 200

        return {
            "message": "이메일 또는 비밀번호가 잘못되었습니다."
        }, 400