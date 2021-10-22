from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from sqlalchemy.orm import backref
# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_manager
# creates hex tokens for our API access
import secrets
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

class User(db.Model):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(150))
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_prod = db.Column(db.Numeric(precision= 10, scale=2))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, make, model, max_speed, dimensions, weight, cost_of_prod, user_token, id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.user_token = user_token

    def set_id(self):
        return (secrets.token_urlsafe())

# Creating our marshaller to pull/create k,v pairs out of Drone attributes
class CarSchema(ma.Schema):
    class Meta:
        # detailing fields(attributes) to be pulled out of our Car class 
        # instance(s) and sent to API call and vice-versa
        fields = ['id', 'model', 'make', 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'series']

Car_schema = CarSchema()
Cars_schema = CarSchema(many=True)