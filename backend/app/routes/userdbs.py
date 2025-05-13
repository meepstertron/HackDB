from flask import Blueprint, jsonify, request
import jwt

from app import db, rq
import logging

import os
from ..models import Users, Databases, Usertables
import re 
from sqlalchemy import text 

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
    
    user = db.session.query(Users).filter_by(id=payload['user_id']).first()
    if not user:
        return jsonify(message='User not found'), 404
    
    dbs = db.session.query(Databases).filter_by(owner=user.id).all()
    
    databases = []
    
    for database in dbs:
        currentdb = {}
        currentdb["id"] = database.id 
        currentdb["name"] = database.name 
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
    
    user = db.session.query(Users).filter_by(id=payload['user_id']).first()
    
    if not user:
        return jsonify(message='User not found'), 404
    
    
    dbs_query = db.session.query(Databases).filter_by(owner=user.id)
    
    if dbs_query.count() >= 5:
        return jsonify(message='User has reached the maximum number of databases'), 403
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify(message='Invalid request: "name" for database is required'), 400
    
    
    new_db = Databases(
        name=data["name"],
        owner=user.id 
    )
    db.session.add(new_db)
    
    try:
        
        db.session.flush()

       
        logical_table_name = "items" 
        new_usertable_metadata = Usertables(
            name=logical_table_name,
            db=new_db.id 
        )
        db.session.add(new_usertable_metadata)
        
        
        db.session.flush()


        sanitized_logical_name = re.sub(r'[^a-zA-Z0-9_]', '', logical_table_name)
        uuid_part = str(new_usertable_metadata.id).replace('-', '_')
        physical_table_name = f"{sanitized_logical_name}_{uuid_part}"
        

        create_table_sql_statement = f"""
        CREATE TABLE '{physical_table_name}' (
            entry_id SERIAL PRIMARY KEY,
            data JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        

        userdb_engine = db.get_engine(bind='userdb')
        with userdb_engine.connect() as connection:
            connection.execute(text(create_table_sql_statement))
            connection.commit()

        db.session.commit()
        
        return jsonify(
            message='Database and default table created successfully', 
            database_id=str(new_db.id),
            table_id=str(new_usertable_metadata.id),
            physical_table_name=physical_table_name
        ), 201

    except Exception as e:
        db.session.rollback() 
        logging.error(f"Error creating database or physical table: {e}")
        return jsonify(message=f'Database creation failed: {str(e)}'), 500



@udb.route('/userdbs/<uuid:db_id>', methods=['GET'])
def get_user_db(db_id):
    """
    get more info about a db
    """
    
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
    
    user = db.session.query(Users).filter_by(id=payload['user_id']).first()
    
    if not user:
        return jsonify(message='User not found'), 404
    
    selected_db = db.session.query(Databases).filter_by(id=db_id, owner=user.id).first()
    if not selected_db:
        return jsonify(message='Database not found'), 404
    
    tables = db.session.query(Usertables).filter_by(db=selected_db.id).all()
    
    
    tablesresult = []
    userdb_engine = db.get_engine(bind='userdb')
    with userdb_engine.connect() as connection:
        for table in tables:
            currenttable = {}
            currenttable["id"] = table.id 
            currenttable["name"] = table.name 
            currenttable["created_at"] = table.created_at.isoformat() if table.created_at else None
            currenttable["rows"] = connection.execute(text(f'SELECT COUNT(*) FROM "{table.name}_{str(table.id).replace("-", "_")}"')).scalar()
            currenttable["physical_table_name"] = f"{table.name}_{str(table.id).replace('-', '_')}"
            # use the table file size from the userdb engine in a readable format so i dont have to convert ti later
            
            
            result = connection.execute(text(f'SELECT pg_size_pretty(pg_total_relation_size(\'"{currenttable["physical_table_name"]}"\')) AS size;'))
            size = result.fetchone()
            if size:
                currenttable["size"] = size[0]
            else:
                currenttable["size"] = "N/A"
            
            currenttable["lastModified"] = None
            tablesresult.append(currenttable)
            
    
    return_payload = {
        
        'database_id': str(selected_db.id),
        'owner_id': str(selected_db.owner),
        'name': selected_db.name,
        'created_at': selected_db.created_at.isoformat() if selected_db.created_at else None,
        'num_tables': len(tables),
        'tables': tablesresult
    }
    
    return jsonify(database=return_payload), 200
    