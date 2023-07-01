
def create_api(api):
    from main_page import MainBanner
    from .user import UserRegister, User, UserLogin
    from .chat import RangeChatList, AllChatList,YMDChatList,NumberChatList
    from .child import Child,ChildList
    from .reservations import GetCounselors, GetPageInfo,MakeReservation,\
        GetUserReservation,GetCounselorReservation, AcceptReservation, RejectReservation,CancleReservation

    #base namespace
    ns_api = api.namespace('api')

    #main page
    ns_main = ns_api.namespace('main')
    ns_main.add_resource(MainBanner, '/banner')

    #child
    api.add_resource(Child, '/child')
    api.add_resource(ChildList, '/childs')

    #chat
    api.add_resource(NumberChatList, '/chats/latest/<string:date>/number/<int:number>')
    api.add_resource(RangeChatList, '/chats/latest/<string:end>/from/<string:begin>')
    api.add_resource(YMDChatList, '/chats/day/<string:day>')
    api.add_resource(AllChatList, '/chats/allday')

    # belonged to user
    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user')
    api.add_resource(UserLogin, '/login')

    # belonged to counselor
    api.add_resource(GetCounselors, '/consultings')
    api.add_resource(GetPageInfo, '/consulting/page/<int:id>')

    #get reservations
    api.add_resource(MakeReservation, '/reservation/make')
    api.add_resource(GetUserReservation, '/reservations/user/<int:id>')
    api.add_resource(GetCounselorReservation, '/reservations/counselor/<int:id>')
    api.add_resource(AcceptReservation, '/reservation/<int:id>/accept')
    api.add_resource(RejectReservation, '/reservation/<int:id>/reject')
    api.add_resource(CancleReservation, '/reservation/<int:id>/cancle')

def create_socketio(sock):
    from .chatnamespace import ChatNamespace
    sock.on_namespace(ChatNamespace('/realchat'))


