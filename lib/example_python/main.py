from python.hackdb import HackDB

hackdb = HackDB(username="user", password="pass", connection_string="hkdb_tkn_1234567890abcdef")


# Accessing hackdb.user calls __getattr__('user') on the HackDB instance.
# This returns a ModelProxy('user', ...) instance.
# Then, .get(...) is called on that ModelProxy instance.
user_data = hackdb.user.get({
    'where': {
        'username': {'equals': "Meep"}
    }
})

print("\nResult:")
print(user_data)

print("-" * 20)

# Another example
posts = hackdb.post.find_many({
    'where': {
        'published': {'equals': True}
    }
})

print("\nResult:")
print(posts)