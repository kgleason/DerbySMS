from DerbySMS import app,manager
from flask.ext.migrate import MigrateCommand
from DerbySMS.models import TwilioConfig
from sys import exit

manager.add_command('db', MigrateCommand)

app.debug = True

if not TwilioConfig.query.all():
    print "There is no twilio config in the database. Please add your account_sid and auth_token into the database."
    exit()

manager.run()