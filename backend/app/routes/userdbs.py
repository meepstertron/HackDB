from flask import Blueprint, jsonify, request
import jwt

from app import db, rq
import logging
from helpers import checkToken, checkTable
import os
from models import Users, Databases, Usertables

signing_secret = os.environ["SLACK_SIGNING_SECRET"]

udb = Blueprint('db', __name__, url_prefix='/api')



@udb.route('/userdbs', methods=['GET'])
def get_user_dbs():
    token = request.cookies.get('jwt')
    if not token:
        return jsonify(message='Unauthorized'), 401
    try:
        payload = jwt.decode(token, signing_secret ,options={"verify_signature": True}, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token expired'), 401
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token'), 401
    except Exception as e:
        logging.error(f"Error decoding JWT: {e}")
        return jsonify(message='Invalid token: Unknown error'), 401
    
    user = db.session.query(Users).filter_by(id=payload["user_id"]).first
    if not user:
        return jsonify(message='User not found'), 404
    
    dbs = db.session.query(Databases).filter_by(owner=user["id"])
    
    databases = []
    
    for database in dbs:
        currentdb = {}
        currentdb["id"] = database["id"]
        currentdb["name"] = database["name"]
        databases.append(currentdb)
        
    return jsonify(databases=databases), 200


@udb.route('/userdbs/create', methods=['POST'])
def create_user_db():
    token = request.cookies.get('jwt')
    if not token:
        return jsonify(message='Unauthorized'), 401
    try:
        payload = jwt.decode(token, signing_secret ,options={"verify_signature": True}, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token expired'), 401
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token'), 401
    except Exception as e:
        logging.error(f"Error decoding JWT: {e}")
        return jsonify(message='Invalid token: Unknown error'), 401
    
    user = db.session.query(Users).filter_by(id=payload["user_id"]).first
    
    if not user:
        return jsonify(message='User not found'), 404
    
    
    dbs = db.session.query(Databases).filter_by(owner=user["id"])
    
    if dbs.count() >= 5:
        return jsonify(message='User has reached the maximum number of databases'), 403
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify(message='Invalid request'), 400
    
    new_db = Databases(
        name=data["name"],
        owner=user["id"]
    )
    
    new_table = Usertables(
        name="items",
        db=new_db["id"]
    )
    
    db.session.add(new_table)
    
    db.session.flush()  # Flush to get the new table ID
    
    result = db.session.execute('', bind=db.get_engine(bind='userdb'))
    
    try:
        db.session.add(new_db)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating database: {e}")
        return jsonify(message='Database creation failed'), 500
    return jsonify(message='Database created successfully'), 201

        
@udb.route('/userdbs/<db_id>', methods=['DELETE'])
def delete_user_db(db_id):
    token = request.cookies.get('jwt')
    if not token:
        return jsonify(message='Unauthorized'), 401
    try:
        payload = jwt.decode(token, signing_secret ,options={"verify_signature": True}, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify(message='Token expired'), 401
    except jwt.InvalidTokenError:
        return jsonify(message='Invalid token'), 401
    except Exception as e:
        logging.error(f"Error decoding JWT: {e}")
        return jsonify(message='Invalid token: Unknown error'), 401
    
    user = db.session.query(Users).filter_by(id=payload["user_id"]).first
    
    if not user:
        return jsonify(message='User not found'), 404
    
    
    dbs = db.session.query(Databases).filter_by(owner=user["id"])
    
    if dbs.count() >= 5:
        return jsonify(message='User has reached the maximum number of databases'), 403
    
    
    db_to_delete = db.session.query(Databases).filter_by(id=db_id, owner=user["id"]).first()
    
    if not db_to_delete:
        return jsonify(message='Database not found or you do not have permission to delete it'), 404
    
    try:
        db.session.delete(db_to_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting database: {e}")
        return jsonify(message='Database deletion failed'), 500
    
    return jsonify(message='Database deleted successfully'), 200    
    
    



    

    
        