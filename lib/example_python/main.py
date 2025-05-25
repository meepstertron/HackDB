import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python.hackdb import HackDB

hackdb = HackDB(token="hkdb_tkn_1dff8dfe-f2a3-41bc-aa02-3d122da57226", base_url="https://condor-willing-buck.ngrok-free.app/api/sdk/v1")


# Accessing hackdb.user calls __getattr__('user') on the HackDB instance.
# This returns a ModelProxy('user', ...) instance.
# Then, .get(...) is called on that ModelProxy instance.
# user_data = hackdb.user.get({
#     'where': {
#         'username': {'equals': "Meep"}
#     }
# })

print(hackdb)
print(hackdb.get_tables())

result = hackdb.Test2.find_many()

print(result)