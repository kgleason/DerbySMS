from DerbySMS import app,manager, socketio
from flask.ext.migrate import MigrateCommand
from sys import exit

manager.add_command('db', MigrateCommand)

app.debug = True

if __name__ == '__main__':
    socketio.run(app)
