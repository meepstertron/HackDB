import time
from flask import Blueprint, jsonify, request
import jwt

from app import db, rq
import logging

import os
from ..models import Users, Databases, Usertables, Tokens
import re 
from sqlalchemy import text 

signing_secret = os.environ["SLACK_SIGNING_SECRET"]

sdk = Blueprint('sdk', __name__, url_prefix='/api/sdk/v1')


@sdk.route('/validatetoken', methods=['GET'])
def validate_token():
    token = request.headers.get('Authorization')
    if not token or not re.match(r"^Bearer hkdb_tkn_[a-f0-9\-]{36}$", token):
        return jsonify({"error": "Invalid or missing token"}), 401


    if db.session.query(Tokens).filter(Tokens.key == token.split(" ")[1]).first():
        return jsonify({"valid": True, "backendversion": "0.0.1-dev"}), 200
    else:
        return jsonify({"valid": False}), 401


@sdk.route('/tables', methods=['GET'])
def get_tables():
    token = request.headers.get('Authorization')
    if not token or not re.match(r"^Bearer hkdb_tkn_[a-f0-9\-]{36}$", token):
        return jsonify({"error": "Invalid or missing token"}), 401
    
    logging.info(f"Received token: {token}")


    token_row = db.session.query(Tokens).filter(Tokens.key == token.split(" ")[1]).first()
    dbid = token_row.dbid if token_row else None
    logging.info(f"Token belongs to dbid: {dbid}")
    if not dbid:
        return jsonify({"error": "token doesnt belong to any db? please report to github issues"}), 404

    tables = db.session.query(Usertables).filter(Usertables.db == dbid).all()
    if not tables:
        return jsonify([]), 404
    table_list = [table.name for table in tables]
    return jsonify(table_list), 200



@sdk.route('/tables/<table_name>/findmany', methods=['GET'])
def get_table_data(table_name):
    token = request.headers.get('Authorization')
    lookup_string = request.args.get('lookup', None)
    if not token or not re.match(r"^Bearer hkdb_tkn_[a-f0-9\-]{36}$", token):
        return jsonify({"error": "Invalid or missing token"}), 401
    
    logging.info(f"Received token: {token}")

    token_row = db.session.query(Tokens).filter(Tokens.key == token.split(" ")[1]).first()
    dbid = token_row.dbid if token_row else None
    logging.info(f"Token belongs to dbid: {dbid}")
    if not dbid:
        return jsonify({"error": "token doesnt belong to any db? please report to github issues"}), 404

    table = db.session.query(Usertables).filter(Usertables.name == table_name, Usertables.db == dbid).first()
    if not table:
        return jsonify({"error": "Table not found"}), 404

    actual_table_name = f"{table.name}_{str(table.id).replace('-', '_')}"

    userdb_engine = db.get_engine(bind='userdb')
    with userdb_engine.connect() as connection:
        if lookup_string:
            print(f"Lookup string provided: {lookup_string}")
        else:
            # if no lookup string is provided, fetch all data bc uhh idk
            result = connection.execute(text(f"SELECT * FROM \"{actual_table_name}\"")).fetchall()
            return jsonify([row._asdict() for row in result]), 200
