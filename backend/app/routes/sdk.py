import time
from flask import Blueprint, jsonify, request
import jwt

import json

from app import db, rq
import logging

from .. import helpers

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
    params = request.args
    lookup_string_param = params.get('lookup_string', None)
    lookup_string = None
    if lookup_string_param is not None:
        lookup_string = json.loads(lookup_string_param)
    logging.info(f"Lookup string: {lookup_string}")
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
        if lookup_string is not None:
            query = text(f"SELECT * FROM \"{actual_table_name}\" " + helpers.whereObjectParser(where=lookup_string))
            result = connection.execute(query).fetchall()
            return jsonify([row._asdict() for row in result]), 200
        else:
            # if no lookup string is provided, fetch all data
            result = connection.execute(text(f"SELECT * FROM \"{actual_table_name}\"")).fetchall()
            return jsonify([row._asdict() for row in result]), 200



@sdk.route('/tables/<table_name>/delete', methods=['DELETE'])
def delete_table_data(table_name):
    token = request.headers.get('Authorization')
    params = request.args
    lookup_string_param = params.get('lookup_string', None)
    lookup_string = None
    if lookup_string_param is not None:
        lookup_string = json.loads(lookup_string_param)
    logging.info(f"Lookup string: {lookup_string}")
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
        if lookup_string is not None:
            query = text(f"DELETE FROM \"{actual_table_name}\" " + helpers.whereObjectParser(where=lookup_string))
            result = connection.execute(query)
            connection.commit()
            return jsonify({"success": True, "message": "Records deleted successfully"}), 200
        else:
            return jsonify({"error": "No lookup string provided"}), 400
        
        
@sdk.route('/tables/<table_name>/create', methods=['POST'])
def create_table_data(table_name):
    token = request.headers.get('Authorization')
    data = request.json.get('data', None)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    data = json.loads(data) if isinstance(data, str) else data
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
        columns = ', '.join([f'"{key}"' for key in data.keys()])
        values = ', '.join([f"'{value}'" for value in data.values()])
        if not len(data) == 0:
            query = text(f"INSERT INTO \"{actual_table_name}\" ({columns}) VALUES ({values})")
        else:
            query = text(f"INSERT INTO \"{actual_table_name}\" DEFAULT VALUES")
        connection.execute(query)
        connection.commit()
        return jsonify({"success": True, "message": "Record created successfully"}), 201
    
    
    
@sdk.route('/tables/<table_name>/count', methods=['GET'])
def count_table_data(table_name):
    token = request.headers.get('Authorization')
    params = request.args
    lookup_string_param = params.get('lookup_string', None)
    lookup_string = None
    if lookup_string_param is not None:
        lookup_string = json.loads(lookup_string_param)
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
        
        if not lookup_string:
            query = text(f"SELECT COUNT(*) FROM \"{actual_table_name}\"")
        else:
            
            query = text(f"SELECT COUNT(*) FROM \"{actual_table_name}\" " + helpers.whereObjectParser(where=lookup_string))
        result = connection.execute(query).scalar()
        return jsonify({"count": result}), 200