from blueprints import db
from flask_restful import fields

class Users(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    response_fields = {
        'user_id': fields.Integer,
        'username': fields.String,
        'email': fields.String,
        'password': fields.String,
        'status': fields.Boolean
    }

    jwt_response_field = {
        'username': fields.String,
        'email': fields.String,
        'status': fields.Boolean
    }

    def __init__(self, username, email, password, status):
        self.username = username
        self.email = email
        self.password = password
        self.status = status

    def __repr__(self):
        return '<User %r>' % self.user_id