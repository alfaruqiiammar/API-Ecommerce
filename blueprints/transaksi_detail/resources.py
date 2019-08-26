import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from . import *
import random
from sqlalchemy import desc
from .models import Transaksi_detail
from flask_jwt_extended import jwt_required

from blueprints import db, app, internal_required


bp_transaksi_detail = Blueprint('transaksi_detail', __name__)
api = Api (bp_transaksi_detail)