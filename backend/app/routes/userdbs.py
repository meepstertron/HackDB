import time
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


@udb.route('/userdbs/<uuid:db_id>/tables', methods=['GET'])
def get_user_db_tables(db_id):
    """
    get all tables in a db and optionally get data from a table
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
    
    request_type = request.args.get('type')
    if request_type == 'lite':
        
        payload = []
        userdb_engine = db.get_engine(bind='userdb')
        with userdb_engine.connect() as connection:
            for table in tables:

                rows = connection.execute(text(f'SELECT COUNT(*) FROM "{table.name}_{str(table.id).replace("-", "_")}"')).scalar()

                returntable = {
                    "id": str(table.id),
                    "name": table.name,
                    "created_at": table.created_at.isoformat() if table.created_at else None,
                    "rows": rows,
                }
                payload.append(returntable)
            return jsonify(tables=payload), 200
        
    if request_type == 'struct':
        #         {
        #     name: "id",
        #     type: "int",
        #     primary: true,
        #     autoIncrement: true,
        #     nullable: false,
        #     default: null,
        #     unique: true,
            
        # },
        # {
        #     name: "name",
        #     type: "text",
        #     primary: false,
        #     autoIncrement: false,
        #     nullable: false,
        #     default: null,
        #     unique: false
        # }
        payload = []
        
        table_id = request.args.get('tableid')
        
        userdb_engine = db.get_engine(bind='userdb')
        with userdb_engine.connect() as connection:
            
            table = db.session.query(Usertables).filter_by(id=table_id, db=selected_db.id).first()
            if not table:
                return jsonify(message='Table not found'), 404
            
            result = connection.execute(text(f"SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = '{table.name}_{str(table.id).replace('-', '_')}'"))
            
            for row in result:
                column_name = row[0]
                data_type = row[1]
                is_nullable = row[2]
                column_default = row[3]
                
                # Check if the column is a primary key
                primary_key_result = connection.execute(text(f"SELECT kcu.column_name FROM information_schema.table_constraints tco JOIN information_schema.key_column_usage kcu ON kcu.constraint_name = tco.constraint_name WHERE tco.table_name = '{table.name}_{str(table.id).replace('-', '_')}' AND tco.constraint_type = 'PRIMARY KEY'"))
                primary_key_columns = [col[0] for col in primary_key_result.fetchall()]
                
                payload.append({
                    "name": column_name,
                    "type": data_type,
                    "primary": column_name in primary_key_columns,
                    "autoIncrement": False,  
                    "nullable": is_nullable == 'YES',
                    "default": column_default,
                    "unique": False 
                })


            return jsonify(payload), 200
    elif request_type == 'data':
        table_id = request.args.get('tableid')
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        if not limit:
            limit = 50
        else: # Ensure limit is an integer so it wont spontaneously combust
            limit = int(limit)
        if not offset:
            offset = 0
        page = request.args.get('page')
        if not page:
            page = 1
        else:
            page = int(page)
        if page > 1:
            offset = (page - 1) * limit
            
        userdb_engine = db.get_engine(bind='userdb')
        with userdb_engine.connect() as connection:
            start_timestamp = time.time()
            table = db.session.query(Usertables).filter_by(id=table_id, db=selected_db.id).first()
            if not table:
                return jsonify(message='Table not found'), 404

            result = connection.execute(text(f"SELECT * FROM \"{table.name}_{str(table.id).replace('-', '_')}\" LIMIT {limit} OFFSET {offset}"))
            #idk this fixed it somehow
            rows = [r._asdict() for r in result]
            time_taken = time.time() - start_timestamp
            time_taken = time_taken * 1000  # Convert to milliseconds
            logging.info(f"Query took {time_taken} seconds")
            return jsonify(rows=rows, time_taken=time_taken), 200
    else:
        return(jsonify(message='Invalid request: "type" must be in range value'), 400)


