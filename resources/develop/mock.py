import datetime

from flask import make_response
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import *

class MakeMock(Resource):

    def get(self):

        user = UserModel.find_by_useremail("test@gmail.com")

        if user :
            resp = make_response({
                "message": "Already made mock"
            })
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


        #make test user
        user = UserModel(
            "테스트유저",
            "test@gmail.com",
            "male",
            datetime.datetime.strptime("1998-01-01","%Y-%m-%d"),
            datetime.datetime.now(),
            "010-1234-5678",
            "서울 강남구",
            "1q2w3e4r"
        )
        user.save_to_db()

        # make test child
        child = ChildModel(
            user.id,
            "김철수",
            datetime.datetime.strptime("2023-01-01","%Y-%m-%d"),
            "female",
            datetime.datetime.now()
        )
        child.save_to_db()

        # make test doll
        doll = DollModel(
            "1q2w3e4r",
            "파트라슈 1호기",
            child.id
        )
        doll.save_to_db()

        # make empty doll
        doll = DollModel(

            "1234",
            "주인없는 파트라슈1",
        )
        doll.save_to_db()

        # make test record
        record = RecordModel(
            child.id,
            user.id,
            datetime.datetime.strptime("2023-07-07", "%Y-%m-%d"),
            datetime.datetime.strptime("11:53:23", "%H:%M:%S"),
            datetime.datetime.strptime("13:02:01", "%H:%M:%S"),
            False
        )
        record.save_to_db()

        #make few chats
        chat = ChatModel(
            record.id,
            user.id,
            datetime.datetime.strptime("2023-07-07 11:53:23", "%Y-%m-%d %H:%M:%S"),
            "doll",
            "안녕, 철수야. 오늘은 어땠니?"
        )
        chat.save_to_db()
        chat = ChatModel(
            record.id,
            user.id,
            datetime.datetime.strptime("2023-07-07 12:01:11", "%Y-%m-%d %H:%M:%S"),
            "child",
            "오늘은 기분이 안좋아"
        )
        chat.save_to_db()
        chat = ChatModel(
            record.id,
            user.id,
            datetime.datetime.strptime("2023-07-07 12:01:20", "%Y-%m-%d %H:%M:%S"),
            "doll",
            "그렇구나... 혹시 왜 그런거 같아?"
        )
        chat.save_to_db()
        chat = ChatModel(
            record.id,
            user.id,
            datetime.datetime.strptime("2023-07-07 13:02:01", "%Y-%m-%d %H:%M:%S"),
            "child",
            "비가 많이와서 그런거같아."
        )
        chat.save_to_db()

        # make category
        category = CategoryModel(
            "ADHD"
        )
        category.save_to_db()
        category = CategoryModel(
            "조울증"
        )
        category.save_to_db()
        category = CategoryModel(
            "불안증세"
        )
        category.save_to_db()
        category = CategoryModel(
            "따돌림"
        )
        category.save_to_db()
        category = CategoryModel(
            "트라우마"
        )
        category.save_to_db()



        # make 준회원 counselor
        counselor=CounselorModel(
            "이준회",
            "010-9999-9999",
            "testcounselor@naver.com",
            "female",
            "경기도 수원시 영통구 영통동",
            "경기도 수원시",
            datetime.datetime.strptime("1989-03-02", "%Y-%m-%d"),
            datetime.datetime.now(),
            _password="a12345678"
        )
        counselor.state = "준회원"
        counselor.save_to_db()

        counselor = CounselorModel(
            "이승대",
            "010-2222-2222",
            "test2counselor2@naver.com",
            "male",
            "경기도 의정부시 호원동 신흥로",
            "경기도 의정부시",
            datetime.datetime.strptime("1992-11-23", "%Y-%m-%d"),
            datetime.datetime.now(),
            _password="a12345678"
        )
        counselor.state = "승인대기"
        counselor.save_to_db()

        category = CategoryModel.find_by_name("ADHD")
        mid_cate = MidCategoryModel(
            category.id,
            counselor.id
        )
        mid_cate.save_to_db()

        category = CategoryModel.find_by_name("불안증세")
        mid_cate = MidCategoryModel(
            category.id,
            counselor.id
        )
        mid_cate.save_to_db()

        license = LicenseModel(
            "심리상담자격증 1급",
            datetime.datetime.strptime("2015-05-30", "%Y-%m-%d"),
            "",
            "한국심리상담협회",
            counselor.id
        )
        license.save_to_db()

        career = CareerModel(
            "허그맘허그인 상담센터",
            datetime.datetime.strptime("2016-10-28", "%Y-%m-%d"),
            "재직",
            "전문 상담사",
            "",
            counselor.id
        )
        career.save_to_db()

        degree = DegreeModel(
            "석사",
            "한양대학교",
            "심리상담학과",
            "놀이치료",
            datetime.datetime.strptime("2014-03-02", "%Y-%m-%d"),
            datetime.datetime.strptime("2016-02-28", "%Y-%m-%d"),
            "졸업",
            "",
            counselor.id
        )
        degree.save_to_db()

        counselor = CounselorModel(
            "이정회",
            "010-5555-5555",
            "test3counselor3@naver.com",
            "male",
            "경기도 성남시 분당구 죽전",
            "경기도 성남시",
            datetime.datetime.strptime("1985-02-12", "%Y-%m-%d"),
            datetime.datetime.now(),
            _intro_title="따듯한 위로를 전하는 이정회입니다.",
            _intro_content="10년간의 심리상담 경력을 바탕으로 어떤 문제든 공감으로 접근합니다.",
            _password="a12345678"
        )
        counselor.state = "정회원"
        counselor.save_to_db()

        category = CategoryModel.find_by_name("ADHD")
        mid_cate = MidCategoryModel(
            category.id,
            counselor.id
        )
        mid_cate.save_to_db()

        category = CategoryModel.find_by_name("따돌림")
        mid_cate = MidCategoryModel(
            category.id,
            counselor.id
        )
        mid_cate.save_to_db()

        category = CategoryModel.find_by_name("조울증")
        mid_cate = MidCategoryModel(
            category.id,
            counselor.id
        )
        mid_cate.save_to_db()

        license = LicenseModel(
            "심리상담자격증 1급",
            datetime.datetime.strptime("2015-05-30", "%Y-%m-%d"),
            "",
            "한국심리상담협회",
            counselor.id
        )
        license.save_to_db()

        career = CareerModel(
            "마인드카페",
            datetime.datetime.strptime("2016-10-28", "%Y-%m-%d"),
            "재직",
            "전문 상담사",
            "",
            counselor.id
        )
        career.save_to_db()

        degree = DegreeModel(
            "박사",
            "연세대학교",
            "심리상담학과",
            "행동치료",
            datetime.datetime.strptime("2014-03-02", "%Y-%m-%d"),
            datetime.datetime.strptime("2016-02-28", "%Y-%m-%d"),
            "졸업",
            "",
            counselor.id
        )
        degree.save_to_db()

        avail_time =AvailableTimeModel(
            "월",
            datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
            datetime.datetime.strptime("18:00:00", "%H:%M:%S"),
            60,
            counselor.id
        )
        avail_time.save_to_db()
        avail_time = AvailableTimeModel(
            "화",
            datetime.datetime.strptime("13:00:00", "%H:%M:%S"),
            datetime.datetime.strptime("18:00:00", "%H:%M:%S"),
            60,
            counselor.id
        )
        avail_time.save_to_db()
        avail_time = AvailableTimeModel(
            "수",
            datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
            datetime.datetime.strptime("18:00:00", "%H:%M:%S"),
            60,
            counselor.id
        )
        avail_time.save_to_db()
        avail_time = AvailableTimeModel(
            "금",
            datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
            datetime.datetime.strptime("18:00:00", "%H:%M:%S"),
            60,
            counselor.id
        )
        avail_time.save_to_db()

        #make reservation
        pre_reservation = PreReservationModel(
            datetime.datetime.strptime("2023-07-10", "%Y-%m-%d"),
            "아이가 자꾸 벽을 주먹으로 쳐요.",
            datetime.datetime.strptime("13:00:00", "%H:%M:%S"),
            "승인완료",
            counselor.id,
            user.id,
            child.id
        )
        pre_reservation.save_to_db()

        post_reservation = PostReservationModel(
            datetime.datetime.strptime("2023-05-05", "%Y-%m-%d"),
            "아이가 저를 자꾸 물어요.",
            datetime.datetime.strptime("15:00:00", "%H:%M:%S"),
            "상담완료",
            False,
            counselor.id,
            user.id,
            child.id
        )
        post_reservation.save_to_db()

        return {
            "message": "Success"
        }

