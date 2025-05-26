from app import db
from .models import Tokens, Usertables, Databases

def checkToken(token: str) -> bool:
    """
    Check if the token is valid.
    """
    
    if not token.startswith('hkdb_tkn_'):
        return False
    
    if not db.session.query(Tokens).filter(Tokens.c.key == token).first():
        return False
    
    return True


def checkTable(table: str, token: str ) -> bool:
    """
    Check if a table name is valid for the token's user and database.
    """
    if not checkToken(token):
        return False
    if not table:
        return False
    
    # get token entry
    tokenentry = db.session.query(Tokens).filter(Tokens.c.key == token).first()
    if not tokenentry:
        return False
    dbid = tokenentry['dbid']
    userid = tokenentry['userid']

    # check that the database is owned by the user
    db_entry = db.session.query(Databases).filter(Databases.id == dbid, Databases.owner == userid).first()
    if not db_entry:
        return False

    # check that the table exists in usertables for this db
    table_entry = db.session.query(Usertables).filter(Usertables.db == dbid, Usertables.name == table).first()
    if not table_entry:
        return False

    return True

def tableToUUID(table: str, token: str) -> str:
    """
    Convert a table name to its UUID.
    """
    if not checkTable(table, token):
        return None
    
    # get token entry
    tokenentry = db.session.query(Tokens).filter(Tokens.c.key == token).first()
    if not tokenentry:
        return None
    dbid = tokenentry['dbid']

    # check that the table exists in usertables for this db
    table_entry = db.session.query(Usertables).filter(Usertables.db == dbid, Usertables.name == table).first()
    if not table_entry:
        return None

    return str(table_entry.id)


def whereObjectParser(where: dict):
    """
     Parse a where object into a WHERE thingie for sql 
    """
    if not where:
        return None
    
    sql_where = "WHERE "
    
    where_list = []
    
    for column, operation in where.items():
        
        if isinstance(operation, dict):
            for operation, value in operation.items():
                if operation == 'equals':
                    where_list.append(f"{column} = '{value}'")
                if operation == 'gt':
                    where_list.append(f"{column} > '{value}'")
                if operation in ['gte', 'ge', 'greaterthanequal']:
                    where_list.append(f"{column} >= '{value}'")
                if operation == 'lt':
                    where_list.append(f"{column} < '{value}'")
                if operation in ['lte', 'le', 'lessthanequal']:
                    where_list.append(f"{column} <= '{value}'")
                if operation == 'contains':
                    where_list.append(f"{column} LIKE '%{value}%'")
                if operation == 'startswith':
                    where_list.append(f"{column} LIKE '{value}%'")
                if operation == 'endswith':
                    where_list.append(f"{column} LIKE '%{value}'")


        else:
            where_list.remove(f"{column} ")
            raise ValueError(f"Invalid operation for column {column}: {operation}")
    sql_where += " AND ".join(where_list)

    return sql_where

