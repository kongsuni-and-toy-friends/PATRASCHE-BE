import requests
from flask_socketio import Namespace, emit, join_room, leave_room, close_room
from flask import session, request
from models.child import ChildModel
from models.chat import ChatModel
from datetime import datetime
from pytz import timezone
import json
import eventlet
import numpy as np
import cv2
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

streaming_config = speech.StreamingRecognitionConfig( # streaming_config = 요청 처리하는 방법을 지정하는 정보 객체
        config=config, interim_results=True # config, interim_result(is_final=true 결과만 반환)
    )

class TestSocket(Namespace):

    def on_connect(self):
        print("Client connected")

        #sessioned= session.get()

    def on_disconnect(self):
        print("Client disconnected")
        #sessioned = session.get()

    def on_audio(self,data):
        requests = (
            speech.StreamingRecognizeRequest(audio_content=data['content'])
        )
        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                print("Final transcript: {}".format(transcript))
            else:
                print("Interim transcript: {}".format(transcript))

    def on_camera(self,data):
        frame = np.array(data['frame'])
        frame = cv2.imdecode(np.fromiter(frame, np.uint8), cv2.IMREAD_COLOR)
