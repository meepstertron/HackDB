import requests
import json
import os
import logging
import re



# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




class ModelProxy:
    def __init__(self, model_name, db_connection):
        self._model_name = model_name
        self._db_connection = db_connection
        print(f"Accessed model: {self._model_name}")

    def _process_query(self, query_dict):
        # In a real scenario, translate this dict into a SQL query,
        # NoSQL query, API call, etc.
        print(f"  Processing query for {self._model_name}: {query_dict}")
        # Simulate database interaction
        where_clause = query_dict.get('where', {})
        if self._model_name == 'user' and where_clause.get('username') == {'equals': 'Meep'}:
            return [{'id': 1, 'username': 'Meep', 'email': 'meep@example.com'}]
        return [] # Default empty result

    def get(self, query_dict):
        print(f"  Executing 'get' operation...")
        results = self._process_query(query_dict)
        # 'get' typically expects one or zero results
        return results[0] if results else None

    def find_many(self, query_dict):
        print(f"  Executing 'find_many' operation...")
        return self._process_query(query_dict)
    
    def delete(self, query_dict):
        print(f"  Executing 'delete' operation...")
        # Simulate deletion
        return True if query_dict else False
    
    def insert(self, data_dict):
        print(f"  Executing 'insert' operation...")
        
        
        
        # Simulate insertion
        return True if data_dict else False
    

    # Add other methods like create, update, delete similarly
    


# --- HackDB Class ---

class HackDB:
    def __init__(self, username:str, password:str, connection_string:str):
        self.username = username 
        self.password = password
        self.connected = False
        if not password or not username:
            self.connection_string = connection_string
            if not connection_string:
                raise ValueError("Either connection_string or username and password must be provided.")
            
            if not connection_string.startswith("hkdb_tkn_"):
                raise ValueError("Invalid connection string format. Must start with 'hkdb_tkn_'")
        else:
            self.connection_string = None
            
        self.base_url = "https://hackdb.hexagonical.ch/api/v1"
        self._db_connection = self # Initialize _db_connection
        
    def __getattr__(self, name):
        # This method is called when an attribute is accessed that doesn't exist.
        # We return a ModelProxy instance initialized with the attribute name.
        print(f"Attempting to access attribute: {name}")
        # You might want to add checks here to ensure 'name' is a valid model
        return ModelProxy(name, self._db_connection)
    
    
    def create_db(self, db_name:str):
        """
        Create a new database with the given name.
        
        Parameters:
        db_name (str): The name of the database to create.
        """
        if not db_name: 
            raise ValueError("Database name cannot be empty.")
        
        print(f"Creating database: {db_name}")
        
        
    def create_table(self, table_name:str, columns:dict):
        """
        Create a new table in the database with the given name and columns.
        
        Parameters:
        table_name (str): The name of the table to create.
        columns (dict): A dictionary where keys are column names and values are their types.
        """
        if not table_name or not columns:
            raise ValueError("Table name and columns cannot be empty.")
        
        print(f"Creating table: {table_name} with columns: {columns}")


