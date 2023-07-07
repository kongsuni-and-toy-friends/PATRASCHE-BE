from db import db
from .child import ChildModel
from .category import CategoryModel
import json

class CounselorModel(db.Model):
    __tablename__ = 'counselor'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    address = db.Column(db.String(80))
    address_range = db.Column(db.String(80))
    intro_title = db.Column(db.String(80))
    intro_content = db.Column(db.String(80))
    thumbnail = db.Column(db.String(80))
    provider = db.Column(db.String(80))
    birth = db.Column(db.DateTime)
    state = db.Column(db.String(80))
    created_at = db.Column(db.DateTime)

    mid_categories = db.relationship('MidCategoryModel', backref='counselor')
    available_times = db.relationship('AvailableTimeModel', backref='counselor')
    careers = db.relationship('CareerModel', backref='counselor')
    licenses = db.relationship('LicenseModel', backref='counselor')
    pre_reservations = db.relationship('PreReservationModel', backref='counselor')
    post_reservations = db.relationship('PostReservationModel', backref='counselor')
    reviews = db.relationship('ReviewModel', backref='counselor')
    #childs = db.relationship('ChildModel', backref='user')
    # reservations = db.relationship('ReservationModel', backref='users')

    def __init__(self, _name,_phone,_email,_gender,_address,_address_range,_intro_title,_intro_content,_thumbnail,_created_at,_password="",_provider=""):
        self.email = _email
        self.password = _password
        self.name = _name
        self.phone = _phone
        self.gender = _gender
        self.address = _address
        self.address_range = _address_range
        self.intro_title = _intro_title
        self.intro_content = _intro_content
        self.thumbnail = _thumbnail
        self.provider = _provider
        self.created_at = _created_at

    def json(self):
        total = 0
        for review in self.reviews:
            total += review.score

        if len(self.reviews) == 0:
            score = 0
        else :
            score = total / len(self.reviews)

        categories_id = [content.category_id for content in self.mid_categories]
        categories = CategoryModel.find_by_ids(categories_id)

        return {
                'id':self.id,
                'name':self.name,
                'thumbnail': self.thumbnail,
                'score': score,
                'category':[cate.name for cate in categories],
                'location':self.address,
                'time': [time.json() for time in self.available_times]
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

    @classmethod
    def find_all(cls):
        return cls.query.all()
