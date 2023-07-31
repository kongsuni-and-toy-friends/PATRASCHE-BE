import requests
from flask_socketio import Namespace, emit, join_room, leave_room, close_room
from flask import session, request
from models.child import ChildModel
from models.chat import ChatModel
from datetime import datetime
from pytz import timezone
import json
import eventlet
import cv2
import numpy as np

cnt = 0
class TestSocket(Namespace):

    def on_connect(self):
        print("Client connected")

        #sessioned= session.get()

    def on_disconnect(self):
        print("Client disconnected")

        cv2.destroyAllWindows()

    def on_camera(self,data):
        global cnt
        frame = np.array(data['frame'])
        time_stamp = data['ts']

        cnt+=1
        if not cnt % 15 :
            print(f"Now {datetime.now().strftime('%H %M %S.%f')} Received {time_stamp}")


        # print(frame.shape)
        frame = cv2.imdecode(np.fromiter(frame, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("img",frame)
        cv2.waitKey(1)
