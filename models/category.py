from db import db
from . import and_


class CategoryModel(db.Model):
    __tablename__ = 'counselor_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    mid_categories = db.relationship('MidCategoryModel', backref='counselor_category')
    #mid_category_id = db.Column(db.Integer, db.ForeignKey('counselor_mid_category.id'))
    #chats = db.relationship('ChatModel', backref='child_record')
    # statistics = db.relationship('StatisticModel', backref='childs')

    def __init__(self,_name):
        self.name = _name

    @classmethod
    def find_all_by_list_name(cls, names):
        return cls.query.filter(cls.name.in_(names)).all()

    @classmethod
    def find_by_serial_number(cls, serial_number):
        return cls.query.filter(cls.serial_number == serial_number).first()

    @classmethod
    def find_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_ids(cls, ids):
        return cls.query.filter(cls.id.in_(ids)).first()

    @classmethod
    def find_by_serial(cls, SN):
        return cls.query.filter_by(serial_number=SN).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class MidCategoryModel(db.Model):
    __tablename__ = 'counselor_mid_category'
    id = db.Column(db.Integer, primary_key=True)

    counselor_id = db.Column(db.Integer, db.ForeignKey('counselor.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('counselor_category.id'))
    # counselors = db.relationship('CounselorModel', backref='counselor_mid_category')
    # categories = db.relationship('CategoryModel', backref='counselor_mid_category')
    # #chats = db.relationship('ChatModel', backref='child_record')
    # statistics = db.relationship('StatisticModel', backref='childs')

    def __init__(self,_name,_counselor_id):
        self.name = _name
        self.counselor_id = _counselor_id


    @classmethod
    def find_by_id_with_list_category_id(cls, category_ids):
        return cls.query.filter(cls.category_id.in_(category_ids)).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter(cls.id.in_(id)).first()

    @classmethod
    def find_by_serial(cls, SN):
        return cls.query.filter_by(serial_number=SN).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()