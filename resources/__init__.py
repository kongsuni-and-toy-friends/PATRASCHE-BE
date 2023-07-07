
def create_api(api):
    from .user import UserKakao, UserRegister, UserDupCheck, UserLogin
    from .child import Child,ChildRecordList
    from .record import Chat
    from .counselor import Counselor,CounselorInfo,CounselorTime
    # from main_page import MainBanner
    # from .chat import RangeChatList, AllChatList,YMDChatList,NumberChatList

    # from .reservations import GetCounselors, GetPageInfo,MakeReservation,\
    #     GetUserReservation,GetCounselorReservation, AcceptReservation, RejectReservation,CancleReservation



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
    ns_counselor = api.namespace('counselors')
    ns_counselor.add_resource(Counselor, '/')
    ns_counselor.add_resource(CounselorInfo, '/<int:counselor_id>')
    ns_counselor.add_resource(CounselorTime, '/<int:counselor_id>/time')
    # api.add_resource(GetCounselors, '/consultings')
    # api.add_resource(GetPageInfo, '/consulting/page/<int:id>')

    # reservations namespace
    # api.add_resource(MakeReservation, '/reservation/make')
    # api.add_resource(GetUserReservation, '/reservations/user/<int:id>')
    # api.add_resource(GetCounselorReservation, '/reservations/counselor/<int:id>')
    # api.add_resource(AcceptReservation, '/reservation/<int:id>/accept')
    # api.add_resource(RejectReservation, '/reservation/<int:id>/reject')
    # api.add_resource(CancleReservation, '/reservation/<int:id>/cancle')

def create_socketio(sock):
    from .chatnamespace import ChatNamespace
    sock.on_namespace(ChatNamespace('/realchat'))


