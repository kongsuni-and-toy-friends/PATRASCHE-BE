from db import db
from . import and_


class MainBannerModel(db.Model):
    __tablename__ = 'main_banner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    thumbnail = db.Column(db.String(80))
    link_to = db.Column(db.String(80))
    priority = db.Column(db.Integer)

    created_at = db.Column(db.Datetime)

    def __init__(self,_name,_thumbnail,_link_to,_priority,_created_at):
        self.name = _name

        self.thumbnail = _thumbnail
        self.link_to = _link_to
        self.priority = _priority
        self.created_at = _created_at


    def json(self):
        return {'info':
                    {
                        'id': self.id, 'name': self.name, 'age':self.age, 'gender':self.gender,'serial_number':self.serial_number,
                        'thumbnail':self.profile
                    },
                'chats':[chat.json() for chat in self.chats]
                }

    @classmethod
    def find_by_name_with_user_id(cls, user_id, name):
        return cls.query.filter(and_(cls.user_id == user_id, cls.name == name)).all()

    @classmethod
    def find_by_serial_number(cls, serial_number):
        return cls.query.filter(cls.serial_number == serial_number).first()

    @classmethod
    def find_by_user_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).first()

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
