from models import *
from flask import render_template, request, session, url_for, redirect
from DerbySMS import app, db, sms
import twilio.twiml

admins = { "+18126069823" : "Kirk",}

@app.route("/sms", methods=['GET', 'POST'])
def inbound_sms():
    """
    Respond to SMS
    """
    
    message = sms.process_sms(r=request)
    
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)
    
@app.errorhandler(404)
def HTTPNotFound(e):
    return render_template('error.html'), 404