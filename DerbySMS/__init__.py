from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../DerbySMS.sqlite3'
try:
    app.config.from_envvar('DERBYSMS_CONFIG')
    app.config['DEBUG'] = True
except Exception, e:
    pass

db = SQLAlchemy()
db.app = app
db.init_app(app)

migrate = Migrate(app,db)
manager = Manager(app)

from DerbySMS import models
from DerbySMS import views
