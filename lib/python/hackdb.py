import requests
import json
import os
import logging
import re
import requests

client_version = "python-0.0.1-dev"  # Version of the HackDB client


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




class ModelProxy:
    def __init__(self, model_name, db_connection):
        self._model_name = model_name
        self._db_connection = db_connection
        if db_connection.debug: print(f"Accessed model: {self._model_name}")




    def find_many(self, where=None, order=None, include=None):
        query_dict = {
            "where": where,
            "order": order,
            "include": include
        }
        # Remove None values from the dictionary
        query_dict = {k: v for k, v in query_dict.items() if v is not None}

        if not self._db_connection.connected:
            raise ValueError("Database connection is not established.")

        response = requests.get(
            f"{self._db_connection.base_url}/tables/{self._model_name}/findmany",
            headers={"Authorization": f"Bearer {self._db_connection.token}"},
            params=query_dict
        )

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to retrieve data: {response.status_code} - {response.text}")
            return []



# --- HackDB Class ---

class HackDB:
    def __init__(self, token:str=None, base_url:str=None):
        self.token = token or os.getenv("HACKDB_TOKEN")
        self.base_url = base_url or "https://hackdb.hexagonical.ch/api/sdk/v1"
        self.debug = False  # Default to not in debug mode
        self.connected = False  # Initialize connected status
        if not self.token:
            raise ValueError("HACKDB_TOKEN must be set either as an argument or as an environment variable.")
        else:
            # Validate the token format
            if not re.match(r"^hkdb_tkn_[a-f0-9\-]{36}$", self.token):
                raise ValueError("Invalid token format.")

            response = requests.get(f"{self.base_url}/validatetoken", headers={"Authorization": f"Bearer {self.token}"})

            if response.status_code == 200:
                self.connected = True
                data = response.json()
                if data.get("valid"):
                    self.connected = True
                    print("Successfully connected to HackDB. (Backend version: {}, Client version: {})".format(data.get("backendversion", "unknown"), client_version))
                else:
                    raise ValueError("Invalid token. Please check your token.")

        self._db_connection = self # Initialize _db_connection

    def __getattr__(self, name):
        
        if not self.connected:
            raise AttributeError(f"HackDB instance is not connected. Cannot access attribute '{name}'.")

        if self.debug: print(f"Attempting to access attribute: {name}")

        return ModelProxy(name, self._db_connection)
    
    

    def __repr__(self):
        if self.connected:
            return f"<HackDB Instance(token={self.token[:16] + '*' * 16}, base_url={self.base_url})>"
        else:
            return "<HackDB Instance (not connected)>"
    # def create_table(self, table_name:str, columns:dict):
    #     """
    #     Create a new table in the database with the given name and columns.
        
    #     Parameters:
    #     table_name (str): The name of the table to create.
    #     columns (dict): A dictionary where keys are column names and values are their types.
    #     """
    #     if not table_name or not columns:
    #         raise ValueError("Table name and columns cannot be empty.")
        
    #     print(f"Creating table: {table_name} with columns: {columns}")
        
    def get_tables(self):
        """
        Retrieve a list of all tables in the database.
        
        Returns:
        list: A list of table names. eg. ["users", "orders", "products"]
        """
        if not self.connected:
            raise ValueError("HackDB instance is not connected. Cannot retrieve tables.")
        response = requests.get(f"{self.base_url}/tables", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to retrieve tables: {response.status_code} - {response.text}")
            return []


