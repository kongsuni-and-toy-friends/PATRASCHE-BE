import datetime

from flask import make_response, request
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import *

class UploadMovie(Resource):
    def post(self):
        """
        TODO:
        동영상 받기
        """
        video_file = request.files['video']
        video_file.save("uploaded_viedo.mp4")

        return "SUCCESS!", 200

class UploadSepMovie(Resource):
    def post(self):
        """
        TODO:
        동영상 받기
        """
        video_file = request.files['video']
        video_file.save("uploaded_video.h264")

        video_file = request.files['audio']
        video_file.save("uploaded_audio.mp3")

        return "SUCCESS!", 200
