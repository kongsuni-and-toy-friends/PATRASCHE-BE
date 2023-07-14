from flask_restx import Namespace

def create_api(api):
    from .auth import UserKakao, UserRegister, UserDupCheck, UserLogin
    from .child import Child,ChildRecordList
    from .record import Chat
    from .counselor import Counselor,CounselorInfo,CounselorTime
    from .reservation import PreReservation, PostReservation, MakeReservation
    from .v2.auth import CounselorRegister, CounselorApprove, CounselorProfile, CounselorLogin, CounselorKakao, CounselorDupCheck
    from .v2.reservation import V2PreReservation,V2PreReservationInfo
    from .develop.develop import MakeMock
    from .mypage import EnrollChild,DollComCheck
    # from main_page import MainBanner
    # from .chat import RangeChatList, AllChatList,YMDChatList,NumberChatList

    # from .reservations import GetCounselors, GetPageInfo,MakeReservation,\
    #     GetUserReservation,GetCounselorReservation, AcceptReservation, RejectReservation,CancleReservation


    # develop namespace
    ns_develop = api.namespace('develop')
    ns_develop.add_resource(MakeMock,'/make_mock')

    # auth namespace
    ns_auth = api.namespace('auth')
    ns_auth.add_resource(UserKakao, '/kakao')
    ns_auth.add_resource(UserRegister, '/register')
    ns_auth.add_resource(UserDupCheck, '/dupcheck')
    ns_auth.add_resource(UserLogin, '/login')
    # ns_auth.add_resource(UserLogin, '/login')
    # ns_auth.add_resource(User, '/user')

    # #main page
    # ns_main = ns_api.namespace('main')
    # ns_main.add_resource(MainBanner, '/banner')

    # child namespace
    ns_child = api.namespace('child')
    ns_child.add_resource(Child, '/')
    ns_child.add_resource(ChildRecordList, '/<int:child_id>/records')
    # api.add_resource(Child, '/child')
    # api.add_resource(ChildList, '/childs')

    # record namespace
    ns_record = api.namespace('record')
    ns_record.add_resource(Chat, '/<int:record_id>/chats')
    # api.add_resource(NumberChatList, '/chats/latest/<string:date>/number/<int:number>')
    # api.add_resource(RangeChatList, '/chats/latest/<string:end>/from/<string:begin>')
    # api.add_resource(YMDChatList, '/chats/day/<string:day>')
    # api.add_resource(AllChatList, '/chats/allday')


    # counselors namespace
    ns_counselor = api.namespace('counselor')
    ns_counselor.add_resource(Counselor, '/')
    ns_counselor.add_resource(CounselorInfo, '/<int:counselor_id>')
    ns_counselor.add_resource(CounselorTime, '/<int:counselor_id>/time')
    # api.add_resource(GetCounselors, '/consultings')
    # api.add_resource(GetPageInfo, '/consulting/page/<int:id>')

    # reservations namespace
    ns_counselor = api.namespace('reservation')
    ns_counselor.add_resource(MakeReservation, '/<int:counselor_id>')
    ns_counselor.add_resource(PreReservation, '/pre')
    ns_counselor.add_resource(PostReservation, '/post')

    # mypage namespace
    ns_mypage = api.namespace('mypage')
    ns_mypage.add_resource(EnrollChild, '/enroll')
    ns_mypage.add_resource(DollComCheck,'/dollcheck')

    # v2 auth namespace
    # #ns_auth.add_resource(UserKakao, '/kakao')
    # ns_auth.add_resource(UserRegister, '/register')
    # ns_auth.add_resource(UserDupCheck, '/dupcheck')
    # ns_auth.add_resource(UserLogin, '/login')
    ns_v2_auth = api.namespace('v2/auth')
    ns_v2_auth.add_resource(CounselorKakao, '/kakao')
    ns_v2_auth.add_resource(CounselorRegister, '/register')
    ns_v2_auth.add_resource(CounselorDupCheck, '/dupcheck')
    ns_v2_auth.add_resource(CounselorLogin, '/login')
    ns_v2_auth.add_resource(CounselorProfile, '/profile')
    ns_v2_auth.add_resource(CounselorApprove, '/approve')

    # v2 reservation namespace
    ns_v2_reservation = api.namespace('v2/reservation')
    ns_v2_reservation.add_resource(V2PreReservation, '/')
    ns_v2_reservation.add_resource(V2PreReservationInfo, '/<int:reservation_id>')



def create_socketio(sock):
    from .develop.sockettest import TestSocket

    #TEST
    sock.on_namespace(TestSocket('/realtime/test'))


