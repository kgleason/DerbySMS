from models import *
from flask import render_template, request, session, url_for, redirect
from DerbySMS import app, db, sms
import twilio.twiml

admins = { "+18126069823" : "Kirk",}

@app.route('/')
def index():
    cur_bets = []
    display_name = ""
    for h in Horse.query.all():
        b = h.get_top_bet_by_id(h.id)
        if b:
            p = Person.query.filter(Person.id == b.person).first()
            if p.firstname:
                display_name = "{0} {1}".format(p.firstname, p.lastname)
            else:
                display_name = p.mobile
                    
            cur_bets.append({
                "h_id" : h.id,
                "horse" : h.name,
                "person" : display_name,
                "amount" : b.amount,
                "ago" : b.created_in_words})
        else:
            cur_bets.append({
                "h_id" : h.id,
                "horse" : h.name,
                "person" : "No one",
                "amount" : "0",
                "ago" : ""})
            
    return render_template('index.html', bets=cur_bets)
    

@app.route("/sms", methods=['GET', 'POST'])
def inbound_sms():
    """
    Respond to SMS
    """
    
    if request.method == "POST":
        message = sms.process_sms(r=request)
    else:
        message = "Sorry, but HTTP {0} is not currently allowed.".format(request.method)
    
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)
    

@app.route('/horses')
def horses():
    h = Horse.all()
    return render_template('horses.html', horses=h)

@app.route('/people')
def people():
    return render_template('people.html', people=Person.all())

@app.route('/horse/<int:id>')
def horse(id):
    horse = Horse.query.filter(Horse.id == id).first()
    bets = Bet.query.filter(Bet.horse == id).order_by(Bet.id.desc())
    display_name = ""
    horse_bets = []
    if bets:
        for bet in bets:
            p = Person.query.filter(Person.id == bet.person).first()
            if p.firstname:
                display_name = "{0} {1}".format(p.firstname, p.lastname)
            else:
                display_name = p.mobile
            
            horse_bets.append({
                "person" : display_name,
                "amount" : bet.amount,
                "ago" :  bet.created_in_words
            })
    else:
        horse_bets = None
    
    return render_template('horse.html', horse=horse, bets=horse_bets)

@app.errorhandler(404)
def HTTPNotFound(e):
    return render_template('error.html'), 404