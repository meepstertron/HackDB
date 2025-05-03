import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')

    # Database Configuration
    db_user = os.environ.get("POSTGRES_USER")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_name = os.environ.get("POSTGRES_DB")
    db_host = os.environ.get("DB_HOST", "db")
    db_port = os.environ.get("DB_PORT", "5432")
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration for the users database
    userdb_user = os.environ.get("USERDB_USER", db_user) 
    userdb_password = os.environ.get("USERDB_PASSWORD", db_password)
    userdb_name = os.environ.get("USERDB_NAME", "hackdb-userdbs")
    userdb_host = os.environ.get("USERDB_HOST", db_host)
    userdb_port = os.environ.get("USERDB_PORT", db_port)
    SQLALCHEMY_BINDS = {
        'userdb': f'postgresql://{userdb_user}:{userdb_password}@{userdb_host}:{userdb_port}/{userdb_name}'
    }
