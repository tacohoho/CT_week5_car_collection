from flask import Flask
from .site.routes import site
#instantiating a new flask app
app = Flask(__name__)

app.register_blueprint(site)