from db import db
from . import and_


class ReviewModel(db.Model):
    __tablename__ = 'counselor_review'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)
    date = db.Column(db.DateTime)
    thumbnail = db.Column(db.String(80))
    content = db.Column(db.String(80))

    counselor_id = db.Column(db.Integer, db.ForeignKey('counselor.id'))
    reservation_id = db.Column(db.Integer, db.ForeignKey('post_reservation.id'))
    #chats = db.relationship('ChatModel', backref='child_record')
    # statistics = db.relationship('StatisticModel', backref='childs')

    def __init__(self,_score,_date,_thumbnail,_content,_counselor_id,_reservation_id):
        self.score = _score
        self.date = _date
        self.thumbnail = _thumbnail
        self.content = _content
        self.counselor_id = _counselor_id
        self.reservation_id = _reservation_id

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
