import time
from flask import Blueprint, jsonify, redirect, request
import jwt

import json

from app import db, rq
import logging

from .. import helpers

import os
from ..models import Users, Databases, Usertables, Tokens, CLIAuthState
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
    user  = db.session.query(Users).filter(Users.id == token_row.userid).first() if token_row else None
    logging.info(f"Token belongs to dbid: {dbid}")
    if not dbid:
        return jsonify({"error": "token doesnt belong to any db? please report to github issues"}), 404
    try:
        helpers.Credits.charge_credits(
            user_id=user.id,
            credits_needed=0.1,
            action="get_tables"
        )
        
    except ValueError:
        logging.error("Insufficient credits to charge this action")
        return jsonify({"error": "Insufficient credits"}), 402
    except Exception as e:
        
        logging.error(f"Error logging credits: {e}")
        return jsonify({"error": "Failed to bill credits"}), 500
    tables = db.session.query(Usertables).filter(Usertables.db == dbid).all()
    if not tables:
        return jsonify([]), 404
    table_list = [table.name for table in tables]
    return jsonify(table_list), 200

@sdk.route('/credits', methods=['GET'])
def get_credits():
    token = request.headers.get('Authorization')
    if not token or not re.match(r"^Bearer hkdb_tkn_[a-f0-9\-]{36}$", token):
        return jsonify({"error": "Invalid or missing token"}), 401
    
    logging.info(f"Received token: {token}")


    token_row = db.session.query(Tokens).filter(Tokens.key == token.split(" ")[1]).first()
    user  = db.session.query(Users).filter(Users.id == token_row.userid).first() if token_row else None
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    
    

@sdk.route('/tables/<table_name>/findmany', methods=['GET'])
def get_table_data(table_name):
    token = request.headers.get('Authorization')
    params = request.args
    lookup_string_param = params.get('lookup_string', None)
    lookup_string = None
    limit_param = params.get('limit', None)
    if limit_param is not None:
        try:
            limit = int(limit_param)
            if limit <= 0:
                return jsonify({"error": "Limit must be a positive integer"}), 400
        except ValueError:
            return jsonify({"error": "Invalid limit value"}), 400
    
    
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

    user = db.session.query(Users).filter(Users.id == token_row.userid).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    try:
        helpers.Credits.charge_credits(
            user_id=user.id,
            credits_needed=0.2,
            action="get_table_data"
        )
        
    except ValueError:
        logging.error("Insufficient credits to charge this action")
        return jsonify({"error": "Insufficient credits"}), 402
    except Exception as e:
        
        logging.error(f"Error logging credits: {e}")
        return jsonify({"error": "Failed to bill credits"}), 500


    userdb_engine = db.get_engine(bind='userdb')
    with userdb_engine.connect() as connection:
        if lookup_string is not None:
            query = text(f"SELECT * FROM \"{actual_table_name}\" LIMIT {limit}" + helpers.whereObjectParser(where=lookup_string))
            result = connection.execute(query).fetchall()
            
        else:
            # if no lookup string is provided, fetch all data
            result = connection.execute(text(f"SELECT * FROM \"{actual_table_name}\" LIMIT {limit}")).fetchall()
            
        connection.commit()

        if not user:
            return jsonify({"error": "User not found"}), 404
        try:
            helpers.Credits.charge_credits(
                user_id=user.id,
                credits_needed=0.2*(len(result)/100),
                action="get_table_data"
            )
            
        except ValueError:
            logging.error("Insufficient credits to charge this action")
            return jsonify({"error": "Insufficient credits"}), 402
        except Exception as e:
            
            logging.error(f"Error logging credits: {e}")
            return jsonify({"error": "Failed to bill credits"}), 500
        
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

    user = db.session.query(Users).filter(Users.id == token_row.userid).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    try:
        helpers.Credits.charge_credits(
            user_id=user.id,
            credits_needed=0.2,
            action="delete_table_data"
        )
        
    except ValueError:
        logging.error("Insufficient credits to charge this action")
        return jsonify({"error": "Insufficient credits"}), 402
    except Exception as e:
        
        logging.error(f"Error logging credits: {e}")
        return jsonify({"error": "Failed to bill credits"}), 500


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
    
    user = db.session.query(Users).filter(Users.id == token_row.userid).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    try:
        helpers.Credits.charge_credits(
            user_id=user.id,
            credits_needed=0.2,
            action="create_table_data"
        )
        
    except ValueError:
        logging.error("Insufficient credits to charge this action")
        return jsonify({"error": "Insufficient credits"}), 402
    except Exception as e:
        
        logging.error(f"Error logging credits: {e}")
        return jsonify({"error": "Failed to bill credits"}), 500
    

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
    
    user = db.session.query(Users).filter(Users.id == token_row.userid).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    try:
        helpers.Credits.charge_credits(
            user_id=user.id,
            credits_needed=0.05,
            action="count_table_data"
        )
        
    except ValueError:
        logging.error("Insufficient credits to charge this action")
        return jsonify({"error": "Insufficient credits"}), 402
    except Exception as e:
        logging.error(f"Error logging credits: {e}")
        return jsonify({"error": "Failed to bill credits"}), 500


    userdb_engine = db.get_engine(bind='userdb')
    with userdb_engine.connect() as connection:
        
        if not lookup_string:
            query = text(f"SELECT COUNT(*) FROM \"{actual_table_name}\"")
        else:
            
            query = text(f"SELECT COUNT(*) FROM \"{actual_table_name}\" " + helpers.whereObjectParser(where=lookup_string))
        result = connection.execute(query).scalar()
        return jsonify({"count": result}), 200
    
    
    
    
# CLI SECTION
@sdk.route('/cli/credits', methods=['GET'])
def cli_credits():
    token = request.headers.get('Authorization')
    method = request.args.get('method', None)
    
    if not method or method not in ['sdk_token', 'slack_oauth', 'hexagonical_auth']:
        return jsonify({"error": "Invalid or missing method"}), 400
    
    if method == 'sdk_token':
        if not token or not re.match(r"^Bearer hkdb_tkn_[a-f0-9\-]{36}$", token):
            return jsonify({"error": "Invalid or missing token"}), 401
        token_row = db.session.query(Tokens).filter(Tokens.key == token.split(" ")[1]).first()
        if not token_row:
            return jsonify({"error": "Token not found"}), 404
    
    if method == 'slack_oauth':
        try:
            if not token or not re.match(r"^Bearer [a-zA-Z0-9\-_.]+$", token):
                return jsonify({"error": "Invalid or missing token"}), 401
            try:
                payload = jwt.decode(token.split(" ")[1], signing_secret, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401
            user_id = payload.get('user_id')
            if not user_id:
                return jsonify({"error": "Invalid token"}), 401
            user = db.session.query(Users).filter(Users.slack_user_id == user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
    if method == 'hexagonical_auth':
        return jsonify({"error": "Hexagonical Auth not implemented yet"}), 501
    
    user = db.session.query(Users).filter(Users.id == token_row.userid if method == 'sdk_token' else user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "credits": user.weekly_allowance,
        "unlimited": user.unlimited,
        "extra_credits": user.purchased_credits,
        "used_this_week": helpers.Credits.get_used_credits_this_week(user.id),
        "used_last_week": helpers.Credits.get_used_credits_last_week(user.id),
        "change_percent": helpers.Credits.get_change_percent(user.id),
        "history": helpers.Credits.get_history(user.id)
    }), 200



@sdk.route('/cli/databases', methods=['GET'])
def cli_databases():
    token = request.headers.get('Authorization')
    if not token or not re.match(r"^Bearer hkdb_tkn_[a-f0-9\-]{36}$", token):
        return jsonify({"error": "Invalid or missing token"}), 401

    token_row = db.session.query(Tokens).filter(Tokens.key == token.split(" ")[1]).first()
    if not token_row:
        return jsonify({"error": "Token not found"}), 404

    user = db.session.query(Users).filter(Users.id == token_row.user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    databases = db.session.query(Databases).filter(Databases.user_id == user.id).all()
    return jsonify({"databases": [db.name for db in databases]}), 200


@sdk.route('/cli/slackauth', methods=['GET'])
def cli_slack_auth():
    instance_id = request.args.get("instanceid")
    
    
    db.session.query(CLIAuthState).filter_by(instance_id=instance_id).delete()
    db.session.commit()
    
        
    state = "cli_"+instance_id

    client_id = os.environ.get("SLACK_CLIENT_ID")
    if not client_id:
        return jsonify({"error": "Server Config error"}), 500
    
    
    oauth_scopes = [
        "identity.basic",
        "identity.email",
    ]
    oauth_scope = ','.join(oauth_scopes)    

    return redirect(f"https://slack.com/oauth/v2/authorize?user_scope={oauth_scope}&client_id={client_id}&state={state}")


@sdk.route("/cli/slackauthresult", methods=["GET"])
def poll_cli_login():
    instance_id = request.args.get("instanceid")

    cli_state = db.session.query(CLIAuthState).filter_by(instance_id=instance_id).first()
    if cli_state and cli_state.verified:
        jwt_token = jwt.encode({"slack_user_id": cli_state.slack_user_id, "user_id": str(cli_state.author_id)}, signing_secret, algorithm="HS256")
        return {"instanceid": instance_id, "token": jwt_token, "status": "verified", "slack_id": cli_state.slack_user_id, "user_id": str(cli_state.author_id)}, 200
    else:
        return {"instanceid": instance_id, "status": "pending"}, 202
    
    

