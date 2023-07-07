from db import db
from . import and_
import datetime


class CareerModel(db.Model):
    __tablename__ = 'counselor_career'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    type = db.Column(db.String(80))
    role = db.Column(db.String(80))
    cert = db.Column(db.String(80))

    counselor_id = db.Column(db.Integer, db.ForeignKey('counselor.id'))
    #chats = db.relationship('ChatModel', backref='child_record')
    # statistics = db.relationship('StatisticModel', backref='childs')

    def __init__(self,_name,_start_date,_type,_role,_cert,_counselor_id,_end_date=None):
        self.name = _name
        self.start_date = _start_date
        self.end_date = _end_date
        self.type = _type
        self.role = _role
        self.cert = _cert
        self.counselor_id = _counselor_id

    def json(self):
        if self.end_date != None:
            end_date = datetime.datetime.strftime(self.end_date,"%Y-%m-%d")
        else:
            end_date = None
        return {
                'name': self.name,
                'start_date':datetime.datetime.strftime(self.start_date,"%Y-%m-%d"),
                'end_date':end_date
                }

    @classmethod
    def find_by_name_with_user_id(cls, user_id, name):
        return cls.query.filter(and_(cls.user_id == user_id, cls.name == name)).all()

    @classmethod
    def find_by_serial_number(cls, serial_number):
        return cls.query.filter(cls.serial_number == serial_number).first()

    @classmethod
    def find_by_counselor_id(cls,counselor_id):
        return cls.query.filter_by(counselor_id=counselor_id).all()

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
