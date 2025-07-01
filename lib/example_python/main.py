import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python.hackdb import HackDB

hackdb = HackDB(token="hkdb_tkn_0dff8dfe-f2a3-41bc-aa02-3d122da57226", base_url="http://localhost:5001/api/sdk/v1")


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

import time

def stress_test(hackdb, num_records=1000):
    print(f"Starting stress test with {num_records} records...")

    # 1. Bulk create
    start = time.time()
    failures = 0
    for i in range(num_records):
        data = {
            "name": f"user_{i}",
            "age": i % 100,
            "is_active": True
        }
        try:
            success = hackdb.Test.create(data)
            if not success:
                print(f"Failed to create record {i}")
                failures += 1
        except Exception as e:
            print(f"Exception at record {i}: {e}")
            failures += 1
        if (i+1) % 100 == 0:
            print(f"Created {i+1} records...")
        
    print(f"Create phase done in {time.time() - start:.2f}s with {failures} failures")

    # 2. Bulk read
    start = time.time()
    try:
        records = hackdb.Test.find_many(limit=num_records)
        print(f"Read {len(records)} records in {time.time() - start:.2f}s")
    except Exception as e:
        print(f"Exception during read: {e}")

    # 3. Bulk delete
    start = time.time()
    try:
        hackdb.Test.delete(where={"name": {"contains": "user_"}})
        print(f"Delete phase done in {time.time() - start:.2f}s")
    except Exception as e:
        print(f"Exception during delete: {e}")

if __name__ == "__main__":
    print(hackdb.Test.count(
        where={
            'age': {'equals': 69} # nice
        }
    ))

    print(hackdb.Test.count())

    # Run stress test
    stress_test(hackdb, num_records=10000)