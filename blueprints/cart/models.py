from blueprints import db
from flask_restful import fields


class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'item.item_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Integer, nullable=False)

    response_fields = {
        'cart_id': fields.Integer,
        'user_id': fields.Integer,
        'item_id': fields.Integer,
        'qty': fields.Integer,
        'harga': fields.Integer
    }

    def __init__(self, item_id, user_id, qty, harga):
        self.item_id = item_id
        self.user_id = user_id
        self.qty = qty
        self.harga = harga

    def __repr__(self):
        return '<Cart %r>' % self.cart_id
