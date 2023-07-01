from db import db
from .child import ChildModel
import json

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    password = db.Column(db.String(80))
    birth = db.Column(db.Datetime)
    thumbnail = db.Column(db.String(80))
    provider = db.Column(db.String(80))
    phone = db.Column(db.String(80))

    created_at = db.Column(db.Datetime)

    childs = db.relationship('ChildModel', backref='user')
    pre_reservations = db.relationship('PreReservationModel', backref='user')
    post_reservations = db.relationship('PostReservationModel', backref='user')
    # reservations = db.relationship('ReservationModel', backref='users')

    def __init__(self, _name,_email,_gender,_birth,_thumbnail,_created_at,_phone,_password="",_provider=""):
        self.name = _name
        self.email = _email
        self.gender = _gender
        self.password = _password
        self.birth = _birth
        self.thumbnail = _thumbnail
        self.provider = _provider
        self.phone = _phone
        self.created_at = _created_at

    def json(self):
        return {
                'id':self.id,
                'name':self.name,
                'user_name':self.user_name,
                'user_type':self.user_type,
                'thumbnail':self.user_profile
            }


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def save_child_data(self,child_name,child_age,child_gender,serial_number):
    #     child = ChildModel(self.id,child_name,child_age,child_gender,serial_number)
    #     child.save_to_db()

    @classmethod
    def find_by_useremail(cls, user_email):
        return cls.query.filter_by(email=user_email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
