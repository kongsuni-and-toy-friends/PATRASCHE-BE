import requests
from flask_socketio import Namespace, emit, join_room, leave_room, close_room
from flask import session, request
from models.child import ChildModel
from models.chat import ChatModel
from datetime import datetime
from pytz import timezone
import json
import eventlet

rooms={
}

#몇번째 시나리오 갈지

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

    # @staticmethod
    # def stat_handler(stat,processed_data,msg):
    #     # emotion handler
    #     if processed_data["Emotion"]:
    #         temp_emotion = json.loads(stat.emotions)
    #         temp_emotion[processed_data['Emotion']] += 1
    #         stat.emotions = json.dumps(temp_emotion)
    #         stat.emotion_score += emotion_weight[processed_data['Emotion']]
    #
    #         # situation handler
    #         if processed_data["Topic"]:
    #             temp_topic = json.loads(stat.situation)
    #             temp_topic[processed_data["Topic"]]["total"] += 1
    #             temp_topic[processed_data["Topic"]]["emotion"][processed_data['Emotion']] += 1
    #             stat.situation = json.dumps(temp_topic)
    #
    #         # # relationship
    #         # temp_relationship = json.loads(stat.relation_ship)
    #         #
    #         # for key in processed_data["NER"]:
    #         #     if key not in temp_relationship.keys():
    #         #         temp_relationship[key] = {}
    #         #         temp_relationship[key]["emotion"] = init_emotion.copy()
    #         #     temp_relationship[key]["emotion"][processed_data["Emotion"]] += 1
    #         # stat.relation_ship = json.dumps(temp_relationship)
    #
    #
    #     # badness handler
    #     if processed_data["Danger_Flag"]:
    #         temp_badwords = json.loads(stat.badwords)
    #         for word in processed_data["Danger_Words"]:
    #             temp_badwords[word] += 1
    #         temp_badsentences = json.loads(stat.bad_sentences)
    #         temp_badsentences['sentences'].append(msg)
    #         stat.badwords = json.dumps(temp_badwords)
    #         stat.bad_sentences = json.dumps(temp_badsentences)
    #
    #
    #
    #
    #     stat.save_to_db()
