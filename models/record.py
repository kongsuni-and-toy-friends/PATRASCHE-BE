from db import db
from . import and_


class RecordModel(db.Model):
    __tablename__ = 'child_record'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Datetime)
    start_time = db.Column(db.Datetime)
    end_time = db.Column(db.Datetime)
    live = db.Column(db.Boolean)

    child_id = db.Column(db.Integer, db.ForeignKey('user_child.id'))
    chats = db.relationship('ChatModel', backref='child_record')
    # statistics = db.relationship('StatisticModel', backref='childs')

    def __init__(self,_child_id,_date,_start,_end,_live):
        self.child_id = _child_id
        self.date = _date
        self.start_time = _start
        self.end_time = _end
        self.live = _live

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