from app import db
from models import t_tokens, Usertables, Databases

def checkToken(token: str) -> bool:
    """
    Check if the token is valid.
    """
    
    if not token.startswith('hkdb_tkn_'):
        return False
    
    if not db.session.query(t_tokens).filter(t_tokens.c.key == token).first():
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
    tokenentry = db.session.query(t_tokens).filter(t_tokens.c.key == token).first()
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
    tokenentry = db.session.query(t_tokens).filter(t_tokens.c.key == token).first()
    if not tokenentry:
        return None
    dbid = tokenentry['dbid']

    # check that the table exists in usertables for this db
    table_entry = db.session.query(Usertables).filter(Usertables.db == dbid, Usertables.name == table).first()
    if not table_entry:
        return None

    return str(table_entry.id)

    