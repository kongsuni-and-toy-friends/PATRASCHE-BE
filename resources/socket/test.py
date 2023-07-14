import requests
from flask_socketio import Namespace, emit, join_room, leave_room, close_room
from flask import session, request
from models.child import ChildModel
from models.chat import ChatModel
from datetime import datetime
from pytz import timezone
import json
import eventlet
from google.cloud import speech

STREAMING_LIMIT = 240000 # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10) # 100ms, 1600

client = speech.SpeechClient() # client = Google Cloud Speech API 객체
config = speech.RecognitionConfig( # config = Recognizer process 객체
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # 인코딩 된 오디오 데이터가 RecognitionAudio로 전송
    sample_rate_hertz=SAMPLE_RATE, # sampling rate
    language_code="ko-KR", # 언어 코드
    enable_automatic_punctuation=True,
    use_enhanced=True,
    max_alternatives=1, # 반환할 인식 가설의 최대 수
)

class TestSocket(Namespace):

    def on_connect(self):
        print("Client connected")

        #sessioned= session.get()

    def on_disconnect(self):
        print("Client disconnected")
        #sessioned = session.get()

    def on_join(self,data):
        print("On Join")


    def on_SEND_MESSAGE(self,data):
        print("On Send")

    @staticmethod
    def time_shift():
        now = datetime.now(timezone('Asia/Seoul'))
        full_date = now.strftime("%Y%m%d%H%M%S")
        day = now.strftime("%Y%m%d")

        ampm = now.strftime('%p')
        ampm_kr = '오전' if ampm == 'AM' else '오후'

        real_time = f"{ampm_kr} {now.strftime('%#I:%M')}"

        return day, full_date, real_time

