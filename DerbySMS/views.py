from DerbySMS.models import *
from flask import render_template, request, session, url_for, redirect
from DerbySMS import app, db, sms, socketio
import twilio.twiml
from flask.ext.socketio import emit
import json

admins = { "+18126069823" : "Kirk",}

@app.route('/')
def index():
    cur_bets = []
    display_name = ""
    for h in Horse.all():
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
                "hsn" : h.shortname,
                "p_id" : p.id,
                "person" : display_name,
                "amount" : b.amount,
                "ago" : "{0} ago".format(b.created_in_words)})
        else:
            cur_bets.append({
                "h_id" : h.id,
                "horse" : h.name,
                "hsn" : h.shortname,
                "p_id" : "0",
                "person" : "No one",
                "amount" : "0",
                "ago" : "Never"})

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


@app.route('/bets')
def bets():
    return render_template('bets.html', bets=Bet.all())

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/person/<int:id>')
def person(id):
    person = Person.query.filter(Person.id == id).first()
    bets = Bet.query.filter(Bet.person == id).order_by(Bet.id.desc())

    person_bets = []
    if bets:
        for bet in bets:
            h = Horse.query.filter(Horse.id == bet.horse).first()

            person_bets.append({
                "amount" : bet.amount,
                "horse" : h.name,
                "ago" : "{0} ago".format(bet.created_in_words)
            })
    else:
        person_bets = None

    return render_template('person.html', person=person, bets=person_bets)

@app.route('/horse/<int:id>')
def horse(id):
    horse = Horse.query.filter(Horse.id == id).first()
    bets = Bet.query.filter(Bet.horse == id).order_by(Bet.id.desc())
    display_name = ""
    horse_bets = []
    if bets:
        for bet in bets:
            p = Person.query.filter(Person.id == bet.person).first()

            horse_bets.append({
                "person" : p.display_name,
                "amount" : bet.amount,
                "ago" :  "{0} ago".format(bet.created_in_words)
            })
    else:
        horse_bets = None

    return render_template('horse.html', horse=horse, bets=horse_bets)

@app.errorhandler(404)
def HTTPNotFound(e):
    return render_template('error.html'), 404

@socketio.on('connect')
def log_connect(message):
    print(message)

@socketio.on('value changed')
def value_changed(message):
    print(message)
    emit('update value', message, broadcast=True)

def update_bet(message):
    print(message)
    socketio.emit('update bet', json.dumps(message))

def insert_row(message):
    socketio.emit('insert row', json.dumps(message))
