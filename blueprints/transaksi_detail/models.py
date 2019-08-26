from blueprints import db
from flask_restful import fields


class Transaksi_detail(db.Model):
    __tablename__ = 'transaksi_detail'
    transaksi_detail_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    transaksi_id = db.Column(db.Integer, db.ForeignKey(
        'transaksi.transaksi_id'), nullable=False, unique=True)
    item_id = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Integer, nullable=False)

    response_fields = {
        'transaksi_detail_id': fields.Integer,
        'transaksi_id': fields.Integer,
        'item_id': fields.Integer,
        'qty': fields.Integer,
        'harga': fields.Integer
    }

    def __init__(self, transaksi_id, item_id, qty, harga):
        self.transaksi_id = transaksi_id
        self.item_id = item_id
        self.qty = qty
        self.harga = harga

    def __repr__(self):
        return '<Transaksi_detail %r>' % self.transaksi_detail_id
