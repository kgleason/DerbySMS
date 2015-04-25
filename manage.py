from DerbySMS import app,manager
from flask.ext.migrate import MigrateCommand
from sys import exit

manager.add_command('db', MigrateCommand)

app.debug = True

manager.run()
