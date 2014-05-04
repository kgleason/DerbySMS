from models import *
from DerbySMS import db
from horse import *
import re
from twilio.rest import TwilioRestClient

def process_sms(r):
    from_number = str(r.values.get('From', None))
    
    person = Person.find_by_mobile(from_number)
    
    if not person:
        # Launch the begugger
        # import pdb; pdb.set_trace()
        person = Person(mobile=from_number)
        db.session.add(person)
        db.session.commit()
        
        send_sms(person, "Reply with 'name firstname lastname' to associate your name with your mobile number.")
    
    text = r.values.get('Body', None)
    words = text.split()
    command = words[0].lower()
    options = {
        "bet" : bet,
        "bid" : bet,
        "name" : intro,
        "status" : status,
        "horse" : horse,
        "turn" : change_betting_status,
    }
    
    try:
        return options[command](person=person, txt=words[1:])
    except KeyError, e:
        return "Unknown command. Please try again."
        

def bet(person, txt):
    try:
        if not betting_running():
            return "I'm sorry. Bidding is currently disabled."
            
        shortname = txt[0].lower()
        bet_amount = txt[1]
        horse = Horse.find_by_nickname(shortname)
    
        if not horse:
            return "Unknown horse {0}".format(shortname)
        
        high_bet = Bet.query.filter(Bet.horse == horse.id).order_by(Bet.amount.desc()).first()
        
        if not high_bet:
            high_bet = Bet(person=person.id, horse=horse.id, amount=0)
    
        if int(bet_amount) > high_bet.amount:
            bet = Bet(person=person.id, horse=horse.id, amount=int(bet_amount))
            db.session.add(bet)
            db.session.commit()
            return "Got your bid on {0} for ${1}".format(horse.name,bet.amount)
        else:
            return "Sorry. Your bid on {0} must be greater than {1}".format(horse.name, high_bet.amount)
    except IndexError, e:
        return "Please try again with `bid shortname amount`\nBoth shortname and amount are required."

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
    except IndexError, e:
        return "Please try again with `name firstname lastname`\nBoth firstname and lastname are required."
        
def status(person, txt):
    word = " ".join(txt)
    bets_by_horse = {}
    bets_by_person = {}
    horse_names = []

    # Get the current high bet for every horse        
    for h in Horse.query.all():
        horse_names.append(h.shortname)
        
        b = h.get_top_bet_by_id(h.id)
        if not b:
            # If there is no bet, then it means that this horse has no bets on it
            continue
        p = Person.query.filter(Person.id == b.person).first()
        
        bets_by_horse[h.shortname] = [h, b, p]
        
        if p.id in bets_by_person:                    
            bets_by_person[p.id].append([h, b, p])
        else:
            bets_by_person[p.id] = [[h, b, p]]
    
    if (not txt) or word.lower() == 'me':
        # Return a list of all of the bets & horses this person for whom this person holds the top bet
        #return "Status by person"
        if person.id in bets_by_person:
            #return str(bets_by_person[person.id])
            message = "You are currently the high bidder with "
            for l in bets_by_person[person.id]:
                #l should be a list
                tmp_horse = l[0]
                tmp_bet = l[1]
                message += "\n{0} for {1}".format(tmp_bet.amount, tmp_horse.name)
            return message
        else:
            return "You are not currently the high bidder for any horses"
        
    elif word in horse_names:
        if word in bets_by_horse:
            hname = bets_by_horse[word][0].name
            bamount = bets_by_horse[word][1].amount
            fname = bets_by_horse[word][2].firstname
            lname = bets_by_horse[word][2].lastname
            
            return "{0} {1} has ${2} on {3}".format(fname, lname, bamount, hname)
        else:
            return "No one has submitted any bids for {0}".format(word)
    else:
        return "I don't know what {0} is".format(word) 
    
def horse(person, txt):
    if not Person.is_admin:
        return "You must be an administrator to change the horses."
    try:
        command = txt[0].lower()    
        if command == 'add' or command == 'new':
            # To add, we need the horses lane, their shortname, and their full name.
            if len(txt[1:]) < 3:
                return "In order to add a horse, you need to use the command as follows\nhorse add lane# nickname full name"
            else:
                return AddHorse(lane=txt[1], nickname=txt[2], fullname=" ".join(txt[3:]))
            
        elif command == 'del':
            return "Deleting horse is not yet supported"
        
        elif command == 'mod':
            #return "Modifying a horse is not yet supported"
            if len(txt[1:]) < 3:
                return "In order to edit a horse, you need to use the command as follows\nhorse mod lane# nickname fullname"
            else:
                return UpdateHorse(lane=txt[1], nickname=txt[2], fullname=" ".join(txt[3:]))
        
        else:
            return "Unknown command for a horse: {0}".format(command)
    
    except IndexError, e:
        return "Please try again with a properly formatted command."
        
def betting_running():
    status = BettingStatus.query.filter(BettingStatus.id == 1).first()
    
    if not status:
        status = BettingStatus(running=False)
        db.session.add(status)
        db.session.commit()
        
    return status.running
    
def change_betting_status(person, txt):
    if txt[0].lower() == "on":
        on = True
    elif txt[0].lower() == "off":
        on = False
    else:
        return "Not sure what to do with {0}".format(txt[0])

    if not person.is_admin:
        return "You must be an administrator to turn the bidding {0}".format(txt[0])
        
        
    status = BettingStatus.query.filter(BettingStatus.id == 1).first()
    
    if not status:
        status = BettingStatus(running=on)
        db.session.add(status)
        db.session.commit()
        return "The bidding has been turned {0}".format(txt[0])
        
    if status.running == on:
        return "The bidding is already {0}".format(txt[0])
    else:
        status.running = on
        db.session.add(status)
        db.session.commit()
        return "The bidding has been turned {0}".format(txt[0])
        
def send_sms(person, message):
    tc = TwilioConfig.query.filter(TwilioConfig.id == 1).first()
    
    if not tc:
        raise Exception("Error reading Twilio config from the database")
    
    client = TwilioRestClient(tc.account_sid, tc.auth_token) 
    
    output = client.messages.create(to=person.mobile, from_="+18125585422",body=message)   