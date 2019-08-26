from blueprints import db
from flask_restful import fields

class Items(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(30), unique=True, nullable=False)
    detail = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    response_fields = {
        'item_id': fields.Integer,
        'nama': fields.String,
        'detail': fields.String,
        'url': fields.String,
        'harga': fields.Integer,
        'total': fields.Integer
    }

    def __init__(self, nama, detail, url, harga, total):
        self.nama = nama
        self.detail = detail
        self.url = url
        self.harga = harga
        self.total = total

    def __repr__(self):
        return '<Item %r>' % self.item_id