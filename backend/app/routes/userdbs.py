from flask import Blueprint, jsonify, request
from app.models import Item
from app import db, rq
import logging
from helpers import checkToken, checkTable

udb = Blueprint('db', __name__, url_prefix='/db')


@udb.route('/get', methods=['GET'])
def get_item():
    token = request.args.get('token')
    if not checkToken(token):
        return jsonify(message='Invalid token'), 401
    


@udb.route('/findmany', methods=['GET'])
def find_many_items():
    token = request.args.get('token')
    table = request.args.get('table')
    if not table:
        return jsonify(message='Table name is required'), 400
    if not checkToken(token):
        return jsonify(message='Invalid token'), 401

    params = request.args.to_dict()
    params.pop('token', None)
    
    if not checkTable(table, token):
        return jsonify(message='Invalid table name for the given token'), 401
    
    
    
    
    

    
        