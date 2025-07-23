# HackDB SDKs

We currently offer the following SDKs. If you have created your own SDK, please contact us or submit a pull request to get it added!

---

## Python SDK

**Installation:**
To install the Python SDK, use the following command:
```bash
pip install hackdb
```

**Getting Started:**
The Python SDK allows you to interact with HackDB seamlessly. Below is an example of how to initialize the SDK and retrieve a list of tables:
```python
import hackdb
from hackdb import HackDB

# Initialize the HackDB client
hackdb = HackDB(token="your_hackdb_token", base_url="http://localhost:5001/api/sdk/v1")

# Print the client instance
print(hackdb)

# Fetch and print the list of tables
print(hackdb.get_tables())
```

**Features:**
- **Connect to HackDB:** Automatically validates your token and establishes a connection.
- **Retrieve Tables:** Fetch a list of all tables in your database.
- **CRUD Operations:** Perform create, read, update, and delete operations on your data.
- **Credits Management:** Check your available credits.

**Error Handling:**
The SDK raises exceptions for invalid tokens, network issues, or API errors. Always wrap your calls in try-except blocks for better error handling:
```python
try:
    tables = hackdb.get_tables()
    print("Tables:", tables)
except Exception as e:
    print("An error occurred:", e)
```

**Advanced Usage:**
You can perform complex queries using the `find_many` method:
```python
# Example: Find users older than 25
users = hackdb.users.find_many(where={"age": {"gt": 25}}, limit=10)
print(users)
```

---

## JavaScript (CDN)

**Get the CDN script:**
Include the HackDB JavaScript SDK in your project by adding the following script tag to your HTML file:
```html
<script src="https://hackdb.hexagonical.ch/hackdb.js"></script>
```

**Getting Started:**
The JavaScript SDK provides an easy way to interact with HackDB in web applications. Below is an example of how to initialize the SDK and connect to the database:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HackDB Test</title>
</head>
<body>
    <h1>HackDB Library Test</h1>
    <script src="https://hackdb.hexagonical.ch/hackdb.js"></script>
    <script>
    (async () => {
        // Initialize the HackDB client
        const db = new HackDB("your_hackdb_token");

        // Connect to HackDB
        const ok = await db.connect();
        if (ok) {
            document.body.innerHTML += "<p>Connected to HackDB!</p>";
        } else {
            document.body.innerHTML += "<p>Failed to connect to HackDB.</p>";
            return;
        }

        // Fetch and display credits
        try {
            const credits = await db.get_credits();
            document.body.innerHTML += `<p>Credits: ${credits}</p>`;
        } catch (err) {
            document.body.innerHTML += `<p>Error fetching credits: ${err.message}</p>`;
        }

        // Fetch and display tables
        try {
            const tables = await db.get_tables();
            document.body.innerHTML += `<p>Tables: ${JSON.stringify(tables)}</p>`;
        } catch (err) {
            document.body.innerHTML += `<p>Error fetching tables: ${err.message}</p>`;
        }
    })();
    </script>
</body>
</html>
```

**Features:**
- **Connect to HackDB:** Validate your token and establish a connection.
- **Retrieve Tables:** Fetch a list of all tables in your database.
- **Credits Management:** Check your available credits.
- **CRUD Operations:** Perform create, read, update, and delete operations on your data.

**Error Handling:**
The SDK provides detailed error messages for invalid tokens, network issues, or API errors. Use try-catch blocks to handle errors gracefully:
```javascript
try {
    const tables = await db.get_tables();
    console.log("Tables:", tables);
} catch (err) {
    console.error("An error occurred:", err);
}
```

**Advanced Usage:**
You can perform complex queries using the `find_many` method:
```javascript
// Example: Find users older than 25
const users = await db.users.find_many({ age: { gt: 25 } }, 10);
console.log(users);
```

---

## Contributing

If you have built an SDK for another language or platform, please open an issue or submit a pull request. We welcome community contributions!