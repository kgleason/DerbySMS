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
                "horse" : h.name,
                "person" : display_name,
                "amount" : b.amount,
                "ago" : b.created_in_words})
        else:
            cur_bets.append({
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
    
@app.route('/horse')
def horse():
    h = Horse.all()
    return render_template('horse.html', horses=h)
@app.route('/person')
def person():
    return render_template('person.html', people=Person.all())
@app.errorhandler(404)
def HTTPNotFound(e):
    return render_template('error.html'), 404