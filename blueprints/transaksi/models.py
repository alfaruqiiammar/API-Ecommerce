from blueprints import db
from flask_restful import fields


class Transactions(db.Model):
    __tablename__ = 'transaksi'
    transaksi_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'item.item_id'), nullable=False)
    total_qty = db.Column(db.Integer, nullable=False)
    total_harga = db.Column(db.Integer, nullable=False)

    response_fields = {
        'transaksi_id': fields.Integer,
        'user_id': fields.Integer,
        'item_id': fields.Integer,
        'total_qty': fields.Integer,
        'total_harga': fields.Integer
    }

    def __init__(self, user_id, item_id, total_qty, total_harga):
        self.user_id = user_id
        self.item_id = item_id
        self.total_qty = total_qty
        self.total_harga = total_harga

    def __repr__(self):
        return '<Transaksi %r>' % self.transaksi_id
