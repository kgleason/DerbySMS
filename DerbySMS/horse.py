from models import *
from DerbySMS import db

def AddHorse(lane, nickname, fullname):
    h = Horse.find_by_lane(lane)
    
    if not h:
        h = Horse.find_by_nickname(nickname)
        if not h:
            h = Horse(name=fullname, shortname=nickname.lower(), lane=lane)
            db.session.add(h)
            db.session.commit()
            
            return "Added {0} as {1} to lane {2}".format(h.name, h.shortname, h.lane)
        else:
            return "There is already a horse named {0}".format(h.shortname)
            
    else:
        return "There is already a horse in lane {0}".format(h.lane)
        
def UpdateHorse(lane, nickname, fullname):
    h = Horse.find_by_lane(lane)
    
    if not h:
        h = Horse.find_by_nickname(nickname)
        
        if not h:
            h = Horse.query.filter(Horse.name == fullname).first()
            
            if not h:
                h = Horse()
                
    h.name = fullname
    h.lane = lane
    h.shortname = nickname
    
    db.session.add(h)
    db.session.commit()
    
    return "Saved {0} as {1} to lane {2}".format(h.name, h.shortname, h.lane)