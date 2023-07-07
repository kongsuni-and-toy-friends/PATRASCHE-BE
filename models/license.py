from db import db
from . import and_


class LicenseModel(db.Model):
    __tablename__ = 'counselor_license'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    cert = db.Column(db.String(80))
    organization = db.Column(db.String(80))

    counselor_id = db.Column(db.Integer, db.ForeignKey('counselor.id'))
    #chats = db.relationship('ChatModel', backref='child_record')
    # statistics = db.relationship('StatisticModel', backref='childs')

    def __init__(self,_name,_date,_cert,_organization,_counselor_id):
        self.name = _name
        self.date = _date
        self.cert = _cert
        self.organization = _organization
        self.counselor_id = _counselor_id

    def json(self):
        return {
                'name': self.name,
                'organization': self.organization
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
