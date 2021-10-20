from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from flask_migrate import Migrate
from .models import db

#instantiating a new flask app
app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)

db.init_app(app)

migrate = Migrate(app, db)