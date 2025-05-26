import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python.hackdb import HackDB

hackdb = HackDB(token="hkdb_tkn_0dff8dfe-f2a3-41bc-aa02-3d122da57226", base_url="https://condor-willing-buck.ngrok-free.app/api/sdk/v1")


print(hackdb)
print(hackdb.get_tables())


# if hackdb.Test2.create({}):
#     print("Record created successfully.")
# else:
#     print("Failed to create record.")



# hackdb.Test2.delete(
#     where={
#         'id': {'gt': 7}
#     }
# )

# result = hackdb.Test2.find_many()
# result2 = hackdb.Test2.find_many(
#     where={
#         'id': {'gt': 5}
#     }
# )
# result3 = hackdb.Test.find_many(
#     where={
#         'name': {'equals': 'bob'},
#         'is_active': {'equals': True}
#     }
# )

# result4 = hackdb.Test.find_many(
#     where={
#         'id': {
#             'equals': 5,
#         }
#     }
# )

# if hackdb.Test.delete(
#     where={
#         'id': {'equals': 5}
#     }
# ):
#     print("Record deleted successfully.")
# else:
#     print("Failed to delete record.")

# print(result)
# print(result2)
# print(len(result3))
# print(result3)


print(hackdb.Test.count(
    where={
        'age': {'equals': 69} # nice
    }
))

print(hackdb.Test.count())