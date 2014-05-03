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
    
    def __init__(self, mobile, firstname=None, lastname=None):
        self.firstname = firstname
        self.lastname = lastname
        self.mobile = mobile
        
    def __repr__(self):
        return "<Person ('%s','%s','%s','%s)>" % (self.id,self.firstname, self.lastname, self.mobile)
    
    @classmethod
    def all(cls):
        return Person.query.order_by(Person.lastname, Person.firstname).all()
            
    @classmethod
    def find_by_mobile(cls, mobile):
        return Person.query.filter(Person.mobile == mobile).first()
    
    @property
    def is_admin(self):
        a = Admin.query.filter(Admin.mobile == self.mobile).first()
        if a:
            return True
        else:
            return False    
            
    @property
    def display_name(self):
        if self.firstname:
            return "{0} {1}".format(self.firstname, self.lastname)
        else:
            return self.mobile
            
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(12), db.ForeignKey(Person.mobile))
    
class Horse(db.Model):
    __tablename__ = 'horse'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    shortname = db.Column(db.String(10))
    lane = db.Column(db.Integer, unique=True)
    
    def __repr__(self):
        return "<Horse ('%s','%s','%s')>" % (self.id, self.name, self.shortname)
    
    @classmethod
    def all(cls):
        return Horse.query.order_by(Horse.lane).all()
        
    @classmethod
    def find_by_lane(cls, lane):
        return Horse.query.filter(Horse.lane == lane).first()
        
    @classmethod
    def find_by_nickname(cls, nname):
        return Horse.query.filter(Horse.shortname == nname).first()
        
    @classmethod
    def get_top_bet_by_id(cls, id):
        return Bet.query.filter(Bet.horse == id).order_by(Bet.id.desc()).first()
        
    @classmethod
    def get_top_bets(cls, id):
        return db.session.query(Bet, Person).select_from(Bet).join(Person).filter(Bet.horse == id).filter(Person.id == Bet.person).order_by(Bet.id.desc()).first()
            
class Bet(db.Model):
    __tablename__ = 'bet_history'
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.Integer, db.ForeignKey(Person.id))
    horse = db.Column(db.Integer, db.ForeignKey(Horse.id))
    amount = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __repr__(self):
        return "<Bet ('%s', '%s', '%s', '%s')>" % (self.id, self.amount, self.person, self.horse)
    
    @classmethod
    def all(cls):
        return Bet.query.order_by(Bet.id.desc()).all()
    
    @classmethod    
    def get_bettor(cls, id):
        p = Person.query.filter(Person.id == id).first()
        return p.display_name
        
    @classmethod
    def get_horse(cls, id):
        h = Horse.query.filter(Horse.id == id).first()
        return h.name
        
    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)
        
    @property
    def placed_by(self):
        return self.get_bettor(self.person)
        
    @property
    def placed_on(self):
        return self.get_horse(self.horse)
        
class BettingStatus(db.Model):
    __tablename__ = 'betting_status'
    id = db.Column(db.Integer, primary_key=True)
    running = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return "<Running ('%s')>" % (self.running)
        
class TwilioConfig(db.Model):
    __tablename__ = 'twilio_config'
    id = db.Column(db.Integer, primary_key=True)
    account_sid = db.Column(db.String(200))
    auth_token = db.Column(db.String(200))
