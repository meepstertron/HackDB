# HackDB SDKs

We currently offer the following SDKs. If you have created your own SDK, please contact us or submit a pull request to get it added!

---

## Python SDK

**Installation:**
```bash
pip install hackdb
```

**Example Usage:**
```python
import hackdb
from hackdb import HackDB

hackdb = HackDB(token="hkdb_tkn_0dff8dfe-f2a3-41bc-aa02-3d122da57226", base_url="http://localhost:5001/api/sdk/v1")

print(hackdb)
print(hackdb.get_tables())
```

---

## JavaScript (CDN)

**Get the CDN script:**  
[https://hackdb.hexagonical.ch/hackdb.js](https://hackdb.hexagonical.ch/hackdb.js)

**Example Usage:**
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
        const db = new HackDB("hkdb_tkn_ceea2285-9144-4c38-9b82-705828cf8252");
        const ok = await db.connect();
        if (ok) {
            document.body.innerHTML += "<p>Connected to HackDB!</p>";
        } else {
            document.body.innerHTML += "<p>Failed to connect to HackDB.</p>";
        }

        db.get_credits().then(credits => {
            document.body.innerHTML += `<p>Credits: ${credits}</p>`;
        }).catch(err => {
            document.body.innerHTML += `<p>Error fetching credits: ${err.message}</p>`;
        });

        db.get_tables().then(tables => {
            document.body.innerHTML += `<p>Tables: ${JSON.stringify(tables)}</p>`;
        }).catch(err => {
            document.body.innerHTML += `<p>Error fetching tables: ${err.message}</p>`;
        });
    })();
    </script>
</body>
</html>
```

---

## Contributing

If you have built an SDK for another language or platform, please open an issue or submit a pull request. We welcome community contributions!

---