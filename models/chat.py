from db import db
from . import and_

class ChatModel(db.Model):
    __tablename__ = 'record_chat'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    chatter = db.Column(db.String(80))
    utterance = db.Column(db.String(80))

    record_id = db.Column(db.Integer, db.ForeignKey('child_record.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, _record_id,_user_id, _date, _chatter,_utterance):
        self.record_id = _record_id
        self.user_id = _user_id
        self.date = _date
        self.chatter = _chatter
        self.utterance = _utterance

    def json(self):
        return {
            'date': self.date,
            'chatter': self.chatter,
            'utterance': self.utterance
        }

    # @classmethod
    # def find_all_by_dateYMD_with_child_id(cls, child_id, day):
    #     return cls.query.filter(and_(cls.child_id == child_id, cls.date_YMD == day)).all()
    #
    # @classmethod
    # def find_by_fulldate_with_child_id(cls, child_id, date):
    #     return cls.query.filter(and_(cls.child_id == child_id, cls.date_YMDHMS == date)).first()
    #
    # @classmethod
    # def find_range_with_child_id(cls, child_id, begin, latest):
    #     return cls.query.filter(and_(cls.date_YMD.between(begin, latest), cls.child_id == child_id)).order_by(
    #         cls.id.desc()).all()
    #
    # @classmethod
    # def find_by_number_with_child_id(cls, child_id, latest, number):
    #     return cls.query.filter(and_(cls.date_YMDHMS < latest, cls.child_id == child_id)).order_by(cls.id.desc()).limit(
    #         number).all()

    @classmethod
    def find_all_by_user_id_with_record_id(cls,user_id,record_id):
        return cls.query.filter(and_(user_id=user_id,record_id=record_id)).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
