from flask_login import UserMixin
from app import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(150))
    profile_image = db.Column(db.String(200))
    backdrop_image = db.Column(db.String(200))
    role = db.Column(db.String(50))
    description = db.Column(db.String(500))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    inputter = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}, Role: {self.role}>'
    
    def get_id(self):
        return self.uid

class Music(db.Model):
    __tablename__ = "music"

    mic = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    image = db.Column(db.String(200))
    file = db.Column(db.String(200))
    featuring_name = db.Column(db.String(200))
    featuring_image_dir = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
    played = db.Column(db.Integer, default=0)
    downloaded = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)
    publish = db.Column(db.Integer, default=0)
    playlist = db.Column(db.String(200))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    inputter = db.Column(db.String(150), nullable=False)
    bpm = db.Column(db.Integer, default=0)
    key = db.Column(db.String(100))
    mood = db.Column(db.String(100))
    instrument = db.Column(db.String(200))
    

    def __repr__(self):
        return f'<Music: {self.name}, Date: {self.date_time}>'


class EmailGroup(db.Model):
    __tablename__ = "email_group"

    gid = db.Column(db.Integer, primary_key=True)
    email_group = db.Column(db.String(200))
    email = db.Column(db.Integer, db.ForeignKey('users.username'))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    inputter = db.Column(db.String(150), nullable=False)
    

class SendEmail(db.Model):
    __tablename__ = "send_email"

    sid = db.Column(db.Integer, primary_key=True)
    email_group = db.Column(db.String(200))
    email = db.Column(db.String(200))
    topic = db.Column(db.String(200))
    body = db.Column(db.String(1000))
    attachement = db.Column(db.String(200))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    inputter = db.Column(db.String(150), nullable=False)

class VerificationEmail(db.Model):
    __tablename__ = "verification_email"

    email = db.Column(db.String(200), primary_key=True)
    verified = db.Column(db.Integer, default=0)
    verification_test =  db.Column(db.Integer, default=0)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    inputter = db.Column(db.String(150), nullable=False)


class PaymentReceived(db.Model):
    __tablename__ = "payment_received"

    pid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    music =  db.Column(db.Integer, db.ForeignKey('music.mic'))
    name = db.Column(db.String(200))
    download_number = db.Column(db.Integer, default=0)
    image = db.Column(db.String(200))
    file = db.Column(db.String(200))
    price = db.Column(db.Integer, default=0)
    bpm = db.Column(db.Integer, default=0)
    key = db.Column(db.String(100))
    mood = db.Column(db.String(100))
    instrument = db.Column(db.String(200))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    inputter = db.Column(db.String(150), nullable=False)

