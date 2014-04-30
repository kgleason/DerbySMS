from sqlalchemy import desc
from DerbySMS import db
import datetime
from webhelpers.date import time_ago_in_words
# Will I need URLify?
from webhelpers.text import urlify

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    mobile = db.Column(db.String(12), unique=True)
    isAdmin = db.Column(db.Boolean, default=False)
    
    def __init__(self, mobile, firstname=None, lastname=None):
        self.firstname = firstname
        self.lastname = lastname
        self.mobile = mobile
        
    def __repr__(self):
        return "<Person ('%s','%s','%s','%s)>" % (self.id,self.firstname, self.lastname, self.mobile)
        
    @classmethod
    def find_by_mobile(cls, mobile):
        return Person.query.filter(Person.mobile == mobile).first()
            
class Horse(db.Model):
    __tablename__ = 'horse'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    shortname = db.Column(db.String(10))
    lane = db.Column(db.Integer, unique=True)
    
    def __repr__(self):
        return "<Horse ('%s','%s','%s')>" % (self.id, self.name, self.shortname)
    
    @classmethod
    def find_by_lane(cls, lane):
        return Horse.query.filter(Horse.lane == lane).first()
        
    @classmethod
    def find_by_nickname(cls, nname):
        return Horse.query.filter(Horse.shortname == nname).first()
            
class Bet(db.Model):
    __tablename__ = 'bet_history'
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.Integer, db.ForeignKey(Person.id))
    horse = db.Column(db.Integer, db.ForeignKey(Horse.id))
    amount = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __repr__(self):
        return "<Bet ('%s', '%s', '%s', '%s')>" % (self.id, self.amount, self.person, self.horse)
    
    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)
        
class BettingStatus(db.Model):
    __tablename__ = 'betting_status'
    id = db.Column(db.Integer, primary_key=True)
    running = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return "<Running ('%s')>" % (self.running)