from app import db,login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    fullname = db.Column(db.String(64))
    position=db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    bookings = db.relationship('Booking', backref='booker', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    roomNum = db.Column(db.String(64))
    ac = db.Column(db.Boolean)
    projector = db.Column(db.Boolean)
    bookings = db.relationship('Booking', backref='room',lazy = 'dynamic')

    def __repr__(self):
        return '<Room {}>'.format(self.roomNum)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    purpose = db.Column(db.String(64),unique = True)
    roomID = db.Column(db.Integer, db.ForeignKey('room.id'))
    bookerID = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    startTime = db.Column(db.Integer)
    endTime = db.Column(db.Integer)
    
    def __repr__(self):
        room = Room.query.filter_by(id=self.roomID).first()
        booker = User.query.filter_by(id=self.bookerID).first()
        return '<Booking Room Number {} for  {} by  {} on {} from {} to {}'.format(room.roomNum,self.purpose,booker.fullname,self.date,self.startTime,self.endTime)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
