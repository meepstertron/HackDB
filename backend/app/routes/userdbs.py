import json
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
        currentdb["tables"] = db.session.query(Usertables).filter_by(db=database.id).count()
        currentdb["size"] = "N/A"
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
        CREATE TABLE "{physical_table_name}" (
            entry_id SERIAL PRIMARY KEY,
            data JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        

        userdb_engine = db.get_engine(bind='userdb')
        with userdb_engine.connect() as connection:
            connection.execute(text(create_table_sql_statement))
            
             # add example data to the table
            example_data = {
                "example_key": "example_value",
                "description": "Thank you for using hackdb"
            }

            connection.execute(
                text(f'INSERT INTO "{physical_table_name}" (data) VALUES (:data)'),
                {"data": json.dumps(example_data)}
            )
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


@udb.route('/userdbs/<uuid:db_id>/tables', methods=['GET', 'POST'])
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
    request_type = request.args.get('type')
    tables = db.session.query(Usertables).filter_by(db=selected_db.id).all()
    if request.method == 'GET':
        
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
            sort = request.args.get('sort') # sort = {'column': 'name', 'direction': 'asc'}
            
            if sort:
                sort_parts = sort.split(',')
                column = sort_parts[0].strip()
                direction = sort_parts[1].strip().lower() if len(sort_parts) > 1 else 'asc'
                # Validate column and direction separately
                if not re.match(r'^[a-zA-Z0-9_]+$', column):
                    return jsonify(message='Invalid sort column'), 400
                if direction not in ['asc', 'desc']:
                    return jsonify(message='Invalid sort direction'), 400
                sort = f'ORDER BY "{column}" {direction.upper()}'
            else:
                sort = ''
            
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

                result = connection.execute(text(f"SELECT * FROM \"{table.name}_{str(table.id).replace('-', '_')}\" {sort} LIMIT {limit} OFFSET {offset}"))
                if result is None:
                    return jsonify(message='No data found'), 404
                if result.returns_rows is False:
                    return jsonify(message='No data found'), 404
                #idk this fixed it somehow
                rows = [r._asdict() for r in result]
                time_taken = time.time() - start_timestamp
                time_taken = time_taken * 1000  # convert to milliseconds
                logging.info(f"Query took {time_taken} seconds")
                return jsonify(rows=rows, time_taken=time_taken), 200
        else:
            return(jsonify(message='Invalid request: "type" must be in range value'), 400)
    elif request.method == 'POST':
        if request_type == 'action.rename':
            """
            Rename a table
            """
            data = request.get_json()
            if not data or 'tableid' not in data or 'newname' not in data:
                return jsonify(message='Invalid request: "tableid" and "newname" are required'), 400
            
            table_id = data['tableid']
            new_name = data['newname']
            
            if not re.match(r'^[a-zA-Z0-9_]+$', new_name):
                return jsonify(message='Invalid table name'), 400
            
            userdb_engine = db.get_engine(bind='userdb')
            with userdb_engine.connect() as connection:
                table = db.session.query(Usertables).filter_by(id=table_id, db=selected_db.id).first()
                if not table:
                    return jsonify(message='Table not found'), 404
                
                # rename the table in the database
                old_physical_name = f"{table.name}_{str(table.id).replace('-', '_')}"
                new_physical_name = f"{new_name}_{str(table.id).replace('-', '_')}"
                
                connection.execute(text(f'ALTER TABLE "{old_physical_name}" RENAME TO "{new_physical_name}"'))
                
                # Update the metadata in the database !!!! IMPORTANTE BECAUSE IT WILL STILL SHOW IN THE UI
                table.name = new_name
                db.session.commit()
                
                return jsonify(message='Table renamed successfully', new_physical_name=new_physical_name), 200
            
        elif request_type == 'action.delete':
            """
            Delete a table
            """
            data = request.get_json()
            if not data or 'tableid' not in data:
                return jsonify(message='Invalid request: "tableid" is required'), 400

            table_id = data['tableid']

            userdb_engine = db.get_engine(bind='userdb')
            with userdb_engine.connect() as connection:
                table = db.session.query(Usertables).filter_by(id=table_id, db=selected_db.id).first()
                if not table:
                    return jsonify(message='Table not found'), 404

                
                physical_name = f"{table.name}_{str(table.id).replace('-', '_')}"
                connection.execute(text(f'DROP TABLE IF EXISTS "{physical_name}"'))
                # delete metadataa
                db.session.delete(table)
                db.session.commit()

                return jsonify(message='Table deleted successfully'), 200
            
        elif request_type == 'action.truncate':
            """"
            Truncate a table aka delete * but faster and the table stays
            """
            userdb_engine = db.get_engine(bind='userdb')
            with userdb_engine.connect() as connection:
                table = db.session.query(Usertables).filter_by(id=table_id, db=selected_db.id).first()
                if not table:
                    return jsonify(message='Table not found'), 404

                physical_name = f"{table.name}_{str(table.id).replace('-', '_')}"
                connection.execute(text(f'TRUNCATE TABLE "{physical_name}"'))
                return jsonify(message='Table truncated successfully'), 200
            
        elif request_type == 'action.duplicate':
            """
            Duplicate a table
            """
            data = request.get_json()
            if not data or 'tableid' not in data:
                return jsonify(message='Invalid request: "tableid" is required'), 400

            table_id = data['tableid']

            userdb_engine = db.get_engine(bind='userdb')
            with userdb_engine.connect() as connection:
                table = db.session.query(Usertables).filter_by(id=table_id, db=selected_db.id).first()
                if not table:
                    return jsonify(message='Table not found'), 404

                new_usertable_metadata = Usertables(
                    name=f"{table.name}_copy",
                    db=selected_db.id
                )
                db.session.add(new_usertable_metadata)
                db.session.flush()  # get new_usertable_metadata.id


                sanitized_logical_name = re.sub(r'[^a-zA-Z0-9_]', '', new_usertable_metadata.name)
                uuid_part = str(new_usertable_metadata.id).replace('-', '_')
                new_physical_name = f"{sanitized_logical_name}_{uuid_part}"
                old_physical_name = f"{re.sub(r'[^a-zA-Z0-9_]', '', table.name)}_{str(table.id).replace('-', '_')}"

                # Duplicate the table structure and data
                connection.execute(text(f'CREATE TABLE "{new_physical_name}" (LIKE "{old_physical_name}" INCLUDING ALL)'))
                connection.execute(text(f'INSERT INTO "{new_physical_name}" SELECT * FROM "{old_physical_name}"'))

                db.session.commit()

                return jsonify(
                    message='Table duplicated successfully',
                    new_table_id=str(new_usertable_metadata.id),
                    new_physical_name=new_physical_name
                ), 201


@udb.route('/userdbs/tokens', methods=['GET', 'POST', 'DELETE'])
def tokens():
    if request.method == 'GET':
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
        
        tokens = []
        
        access_tokens = db.session.query(Tokens).filter_by(userid=user.id).all()
        for token in access_tokens:
            currenttoken = {}
            currenttoken["id"] = token.id 
            currenttoken["databaseid"] = token.dbid
            currenttoken["database"] = db.session.query(Databases).filter_by(id=token.dbid).first().name
            currenttoken["name"] = token.name
            currenttoken["token"] = token.key
            currenttoken["created_at"] = token.created_at.isoformat() if token.created_at else None
            tokens.append(currenttoken)

        return jsonify(tokens=tokens), 200

    elif request.method == 'POST':
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
        
        data = request.get_json()
        if not data or 'name' not in data or 'dbid' not in data:
            return jsonify(message='Invalid request: "name" and "dbid" are required'), 400
        
        dbid = data['dbid']
        selected_db = db.session.query(Databases).filter_by(id=dbid, owner=user.id).first()
        
        if not selected_db:
            return jsonify(message='Database not found'), 404
        
        new_token = Tokens(
            name=data['name'],
            key=jwt.encode({'user_id': user.id, 'db_id': dbid}, signing_secret, algorithm='HS256'),
            userid=user.id,
            dbid=dbid
        )
        
        db.session.add(new_token)
        db.session.commit()
        
        return jsonify(message='Token created successfully', token=new_token.key), 201
    elif request.method == 'DELETE':
        
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
        
        data = request.get_json()
        if not data or 'token_id' not in data:
            return jsonify(message='Invalid request: "token_id" is required'), 400
        
        token_to_delete = db.session.query(Tokens).filter_by(id=data['token_id'], owner=user.id).first()
        
        if not token_to_delete:
            return jsonify(message='Token not found'), 404
        
        db.session.delete(token_to_delete)
        db.session.commit()
        
        return jsonify(message='Token deleted successfully'), 200
    
    
@udb.route('/userdbs/<uuid:db_id>/commit', methods=['POST'])
def commit_user_db(db_id):
    """
    commit a db
    """
    
    token = request.cookies.get('jwt')
    commitlist = request.get_json(). get('commits', [])
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
    
    if not commitlist:
        return jsonify(message='Invalid request: "commits" is required (this means my goofy ahh backend has messed up, report to github)'), 400
    
    for commit in commitlist:
        job = rq.enqueue('app.tasks.commit_change', commit, db_id, user.id)
        commit['job_id'] = job.id
    return jsonify(message='Commit queued successfully', jobs=commitlist), 200



@udb.route('/userdbs/poll', methods=['GET'])
def poll_information():
    """
    poll for information about commit tasks (and more soon)
    """
    method = request.args.get('method')
    
    if method == 'commit_result':
        """
        Get how many of the commits have been processed and how many have succeeded/ failed
        """
        job_ids = request.args.getlist('job_ids')
        if not job_ids:
            return jsonify(message='Invalid request: "job_ids" is required'), 400
        
        results = []
        for job_id in job_ids:
            job = rq.get_job(job_id)
            if job:
                results.append({
                    'job_id': job.id,
                    'status': job.get_status(),
                    'result': job.result
                })
            else:
                results.append({
                    'job_id': job_id,
                    'status': 'not_found',
                    'result': None
                })
        failed = any(result['status'] == 'failed' for result in results)
        failed += any(result['result'] == 'failed' for result in results)
        pending = any(result['status'] == 'queued' for result in results)
        return jsonify(results=results, failed=failed, pending=pending, total=len(results)), 200
