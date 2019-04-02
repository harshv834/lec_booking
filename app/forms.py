from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField,SelectMultipleField,DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import *
import datetime
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(),Email()])
    fullname = StringField('Fullname', validators = [DataRequired()])
    position = StringField('Position', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class RoomChoices(object):
    def __iter__(self):
        rooms = Room.query.all()
        rooms = [(room.id, room.roomNum) for room in rooms]
        for room in rooms:
            yield room

class BookingForm(FlaskForm):
    purpose = StringField('Booking Purpose', validators = [DataRequired()])
    rooms = SelectField('Choose Room', coerce=int, choices = RoomChoices())
    date = DateField('Choose Date', format="%m/%d/%Y",validators=[DataRequired()])
    startTime = SelectField('Choose starting time(24 hr clock)',coerce=int,choices=[(i,i) for i in range(8,19)])
    endTime = SelectField('Choose starting time(24 hr clock)',coerce=int,choices=[(i,i) for i in range(8,19)])
    submit = SubmitField('Book')

    def validate_date(self,date):
        if self.date.data<datetime.datetime.now().date():
            raise ValidationError('Bookings not allowed for same or previous days')
    def validate_time(self,startTime,endTime):
        if self.startTime.data < self.endTime.data:
            raise ValidationError(' Endtime before starttime')

    def validate_intersections(self,date,startTime,endTime):
        bookings = Booking.query.filter_by(roomNum=rooms.data).all()
        flag = False
        for booking in bookings:
            if self.date.data == booking.date:
                if self.startTime.data <= booking.endTime and self.startTime.data >= booking.startTime:
                    flag = True
                    break
                if self.endTime.data <= booking.endTime and self.endTime.data >= booking.startTime:
                    flag = True
                    break
        if flag:
            raise ValidationError("Booking Clash. Check for room availability")

class BookingChoices(object):
    def __iter__(self):
        bookings = Booking.query.filter_by(bookerID=current_user.id).all()
        bookings = [(booking.id,"{} in Room  {} on {} from {} to {}".format(booking.id,Room.query.filter_by(id=booking.roomID).first().roomNum,booking.date,booking.startTime,booking.endTime)) for booking in bookings]
        for booking in bookings:
            yield booking

class CancelBookingForm(FlaskForm):
    ids = SelectMultipleField('Choose Booking to cancel', coerce=int, choices=BookingChoices())
    submit = SubmitField('Cancel')



class RoomOccupationForm(FlaskForm):
    date = DateField('Choose Date', format="%d/%m/%Y", validators=[DataRequired()])
    submit = SubmitField('Check')


