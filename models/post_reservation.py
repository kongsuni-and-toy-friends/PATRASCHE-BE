from db import db
from . import and_
from .counselor import CounselorModel
from .child import ChildModel
from .review import ReviewModel
import datetime

class PostReservationModel(db.Model):
    __tablename__ = 'post_reservation'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    problem = db.Column(db.String(80))
    start_time = db.Column(db.DateTime)
    state = db.Column(db.String(80))
    has_review = db.Column(db.Boolean)

    review = db.relationship('ReviewModel', backref='post_reservation')
    counselor_id = db.Column(db.Integer, db.ForeignKey('counselor.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    child_id = db.Column(db.Integer)
    #chats = db.relationship('ChatModel', backref='child_record')
    # statistics = db.relationship('StatisticModel', backref='childs')

    def __init__(self,_date,_problem,_start_time,_state,_has_review,_counselor_id,_user_id,_child_id):
        self.date = _date
        self.problem = _problem
        self.start_time = _start_time
        self.state = _state
        self.has_review = _has_review
        self.counselor_id = _counselor_id
        self.user_id = _user_id
        self.child_id = _child_id

    def json(self):
        counselor = CounselorModel.find_by_id(self.counselor_id)
        child = ChildModel.find_by_id(self.child_id)

        review = ReviewModel.find_by_reservation_id(self.id)

        if review :
            review_id = review.id
        else:
            review_id = None

        return {
            'id': self.id,
            'date': datetime.datetime.strftime(self.date,"%Y-%m-%d"),
            'start':datetime.datetime.strftime(self.start_time,"%H:%M:%S"),
            'counselor': counselor.name,
            'child': child.name,
            'problem': self.problem,
            'has_review': self.has_review,
            'review_id': review_id
        }

    @classmethod
    def find_by_name_with_user_id(cls, user_id, name):
        return cls.query.filter(and_(cls.user_id == user_id, cls.name == name)).all()

    @classmethod
    def find_by_serial_number(cls, serial_number):
        return cls.query.filter(cls.serial_number == serial_number).first()

    @classmethod
    def find_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_serial(cls, SN):
        return cls.query.filter_by(serial_number=SN).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
