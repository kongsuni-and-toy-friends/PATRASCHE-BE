from db import db
from . import and_
import datetime

class RecordModel(db.Model):
    __tablename__ = 'child_record'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('user_child.id'))
    chats = db.relationship('ChatModel', backref='child_record')
    # statistics = db.relationship('StatisticModel', backref='childs')

    def __init__(self,_child_id,_user_id,_date,_start,_end,_live):
        self.child_id = _child_id
        self.user_id = _user_id
        self.date = _date
        self.start_time = _start
        self.end_time = _end
        self.live = _live

    def json(self):
        return {
                    'id': self.id,
                    'date': datetime.datetime.strftime(self.date,"%Y-%m-%d"),
                    'start_time':datetime.datetime.strftime(self.start_time,"%H:%M:%S"),
                    'end_time':datetime.datetime.strftime(self.end_time,"%H:%M:%S"),
                    'live':self.live
                }

    @classmethod
    def find_all_by_child_id_with_user_id(cls, child_id,user_id):
        return cls.query.filter(and_(cls.user_id == user_id, cls.child_id == child_id)).all()


    def find_all_by_child_id(cls,child_id):
        return cls.query.filter_by(child_id=child_id).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
