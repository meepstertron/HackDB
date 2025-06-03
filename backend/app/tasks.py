from rq import get_current_job
import time

import logging
from app import db
from flask import current_app
import os
from .models import Users, Databases, Usertables, Tokens
import re 
from sqlalchemy import text 
from . import helpers


# me testing the task queue
def example_task(x, y):
    job = get_current_job()
    print(f"Running example_task with args: {x}, {y}")
    time.sleep(2)  
    result = x + y
    print(f"Task result: {result}")
    return result



# [
#     {
#         "where": {
#             "age": {
#                 "equals": 72
#             },
#             "created_at": {
#                 "equals": "Sun, 18 May 2025 20:23:36 GMT"
#             },
#             "email": {
#                 "equals": "user_2@example.com"
#             },
#             "id": {
#                 "equals": 2
#             },
#             "name": {
#                 "equals": "User_2"
#             },
#             "hiddenRowIDforFrontend": {
#                 "equals": 0
#             }
#         },
#         "column": "is_active",
#         "oldValue": true,
#         "newValue": false,
#         "table": "98ef25bf-b84d-47a3-8d44-27d17b74f6c2",
#         "type": "edit",
#         "timestamp": "2025-05-28T15:46:07.812Z"
#     }
# ]

def commit_change(change:dict, db_id, user_id):
    from app import create_app # get the flask thingie because it will combust if it doesnt get db :pf:

    app = current_app._get_current_object() if current_app else create_app() #get the main app or make a new tinesy little baby app that ig has the db 
    with app.app_context():
        print(f"Running commit_change with change: {change}")
        userdb_engine = db.get_engine(bind='userdb')
        table_id = change.get("table")
        logical_table = db.session.query(Usertables).filter_by(id=table_id).first()
        if not db_id:
            raise ValueError("Change must include a 'db_id' key with the database ID.")

        actual_table_name = f"{logical_table.name}_{str(logical_table.id).replace('-', '_')}" if logical_table else None

        if not table_id:
            raise ValueError("Change must include a 'table' key with the table ID.")
        
        where = helpers.whereObjectParser(change.get("where", {}))

        if change.get("type") == "edit":
            column = change.get("column")
            old_value = change.get("oldValue")
            new_value = change.get("newValue")
            
            if column is None or new_value is None:
                raise ValueError("Change of type 'edit' must include 'column', 'oldValue', and 'newValue' keys.")
            
            if old_value is None:
                old_value_clause = f"{column} IS NULL"
                params = {"new_value": new_value}
            else:
                old_value_clause = f"{column} = :old_value"
                params = {"new_value": new_value, "old_value": old_value}
            query = text(f"""
                UPDATE "{actual_table_name}" 
                SET {column} = :new_value 
                {where} AND {old_value_clause}
            """)
            
            
            # ass code lol
        elif change.get("type") == "delete":
            # remove hiddenRowIDforFrontend from where clause
            # if where:
            #     del where["hiddenRowIDforFrontend"]
            query = text(f"""
                DELETE FROM "{actual_table_name}" 
                WHERE {where}
            """)
            params = {}

        elif change.get("type") == "delete_column":
            column = change.get("column")
            query = text(f"""
                ALTER TABLE "{actual_table_name}" 
                DROP COLUMN {column}
            """)
            params = {}

        else:
            raise ValueError(f"Unsupported change type: {change.get('type')}")
        
        with userdb_engine.connect() as connection:
            result = connection.execute(query, params)
            connection.commit()
            print(f"Query executed successfully: {query}, {params}")
            if result:
                print(f"affected rows: {result.rowcount}")
                if result.rowcount == 0:
                    print("No rows were affected by the query.")
                    return "failed"

        return change