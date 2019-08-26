from blueprints import db
from flask_restful import fields

class Admins(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    # statusAdmin = db.Column(db.Boolean, nullable=False)

    response_fields = {
        'admin': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        # 'statusAdmin': fields.Boolean
    }

    jwt_response_field = {
        'username': fields.String,
        # 'statusAdmin': fields.Boolean
    }

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # self.statusAdmin = statusAdmin

    def __repr__(self):
        return '<Admin %r>' % self.admin_id