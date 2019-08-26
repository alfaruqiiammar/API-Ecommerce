from blueprints import db
from flask_restful import fields

class User_details(db.Model):
    __tablename__ = 'user_details'
    user_details_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(30), unique=True, nullable=False)
    alamat = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    nomor_hp = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, unique=True)

    response_fields = {
        'user_details_id': fields.Integer,
        'nama': fields.String,
        'alamat': fields.String,
        'email': fields.String,
        'nomor_hp': fields.String,
        'user_id': fields.Integer
    }

    def __init__(self, nama, alamat, email, nomor_hp, user_id):
        self.nama = nama
        self.alamat = alamat
        self.email = email
        self.nomor_hp = nomor_hp
        self.user_id = user_id

    def __repr__(self):
        return '<User %r>' % self.user_id