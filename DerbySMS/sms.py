from models import *
from DerbySMS import db

def process_sms(r):
    from_number = str(r.values.get('From', None))
    
    person = Person.find_by_mobile(from_number)
    
    if not person:
        # Launch the begugger
        # import pdb; pdb.set_trace()
        person = Person(mobile=from_number)
        db.session.add(person)
        db.session.commit()
    
    text = r.values.get('Body', None)
    words = text.split()
    command = words[0]
    options = {
        "bet" : bet,
        "Bet" : bet,
        "name" : intro,
        "Name" : intro,
        "status" : status,
        "Status" : status,
        "horse" : horse,
        "Horse" : horse,
    }
    
    try:
        return options[command](person=person, txt=words[1:])
    except KeyError, e:
        return "Unknown command. Please try again."
        
def bet(person, txt):
    horse_shortname = txt[0]
    bet_amount = txt[1]
    horse = Horse.query.filter_by(shortname=horse_shortname)
    
    if not horse:
        return "Unknown horse {0}".format(horse_shortname)
        
    high_bet = Bet.query.filter_by(horse=horse.id).order_by(Bet.amount.desc()).first()
    
    if int(bet_amount) > high_bet.amount:
        bet = Bet(person=person.id, horse=horse.id, amount=int(bet_amount))
        db.session.add(bet)
        db.session.commit()
        return "Got your bet on {0} for ${1}".format(horse.name,bet.amount)
    else:
        return "Sorry. Your bet on {0} must be greater than {1}".format(horse.name, high_bet.amount)

def intro(person, txt):
    try:
        fname = txt[0]
        lname = txt[1]
        # Check to see if the name values are null:
        if not person.firstname and not person.lastname:
            # Both names are None. 
            person.firstname = fname
            person.lastname = lname
            db.session.add(person)
            db.session.commit()
            return "You are saved as {0} {1} for mobile {2}".format(person.firstname, person.lastname, person.mobile)
        else:
            return "You are not allowed to change your name after it has been set."
    except Exception, e:
        return "Please try again with `name firstname lastname`\nBoth firstname and lastname are required."
        
def status(person, txt):
    return "Got status command"
    
def horse(person, txt):
    return "Got horse commands"        