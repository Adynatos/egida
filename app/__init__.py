import config
from flask import Flask
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config)

app.config
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import views, models
