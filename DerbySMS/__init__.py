from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLITE_DB_FILE
app.config['DEBUG'] = True
app.config.from_number = config.FROM_NUMBER

db = SQLAlchemy()
db.app = app
db.init_app(app)

migrate = Migrate(app,db)
manager = Manager(app)

from DerbySMS import models
from DerbySMS import views
