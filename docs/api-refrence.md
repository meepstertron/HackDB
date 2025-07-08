# API Refrence
Beware. these are for SDKs and may cost credits to perform.



## [GET] /api/sdk/v1/validatetoken

**Description:**  
Validates a API token


**Request**
- **Headers:**  
  - Authorization: Token to validate (starts with hkdb_tkn_)


**Response**
- **Status:** [200]
- **Body:**  
  ```json
  {
    "valid": True,
    "backendversion": "1.0.0"
  }
  ```

**Errors**
- [401]: Token isnt valid

---

## [GET] /api/sdk/v1/tables

**Description:**  
Get a list of table names of the DB associated with the token

**Cost**: 0.02 Units

**Request**
- **Headers:**  
  - Authorization: API Token (starts with hkdb_tkn_)

**Response**
- **Status:** [200]
- **Body:**  
  ```json
    ["table1", "table2", "table3"]
  ```

**Errors**
- [401]: Token isnt valid
- [404]: No tables found
- [402]: Insufficient Credits
- [500]: Error Processing request

---

## [GET] /api/sdk/v1/credits

**Description:**  
Get the ammount of availible credits for the token

**Request**
- **Headers:**  
  - Authorization: API Token (starts with hkdb_tkn_)


**Response**
- **Status:** [200]
- **Body:**  
  ```json
  {
    "credits": 100
  }
  ```

**Errors**
- [404]: User not found
- [401]: Token isnt valid

---

## [GET] /api/sdk/v1/tables/<table_name>/findmany

**Description:**  
Gets rows from a table associated to the db of the token using a where object and a limit ammound of rows to return

**Cost**: 0.2 Units per 100 rows returned

**Request**
- **Headers:**  
  - Authorization: API Token (starts with hkdb_tkn_)
- **Query Parameters:**  
  - lookup_string: a where json object struct: {"column name": {"op": "value"}} (optional)
  - limit: Limit the ammount of rows to get. default: 50 (optional)


**Response**
- **Status:** [200]
- **Body:**  
  ```json
    [
        {"id": 1, "name": "jan"}, {"id": 2, "name": "alice"}
    ] // List of rows found in table
  
  ```

**Errors**
- [401]: Token isnt valid
- [404]: User/Table/db not found
- [402]: Insufficient Credits
- [500]: Error Processing request

---

## [DELETE] /api/sdk/v1/tables/<table_name>/delete

**Description:**  
Delete rows matching the where object

**Request**
- **Headers:**  
  - Authorization: API Token (starts with hkdb_tkn_)
- **Query Parameters:**  
  - lookup_string: a where json object struct: {"column name": {"op": "value"}} (optional)

**Response**
- **Status:** [200]
- **Body:**  
  ```json
    {
        "success": True, 
        "message": "Records deleted successfully"
    }
  ```

**Errors**
- [400]: No lookup string provided 
- [402]: Insufficient Credits
- [500]: Error Processing request
- [404]: User/Table/db not found

---

## [POST] /api/sdk/v1/tables/<table_name>/create

**Description:**  
If a object is provided it will try to add it to the table provided filling empty fields with null or default if availible providing a list will add multiple records for the price of one

**Request**
- **Headers:**  
  - Authorization: API Token (starts with hkdb_tkn_)
- **Body:**  
  ```json
  {
    "name": "test"
  }
  ```

**Response**
- **Status:** [200]
- **Body:**  
  ```json
  {
    "success": True,
    "message": "Record created successfully"
  }
  ```

**Errors**
- [402]: Insufficient Credits
- [500]: Error Processing request
- [404]: User/Table/db not found

---

## [METHOD] /api/sdk/v1/tables/<table_name>/count

**Description:**  
Count the ammount the where string affects.

**Request**
- **Headers:**  
  - Authorization: API Token (starts with hkdb_tkn_)
- **Query Parameters:**  
  - lookup_string: a where json object struct: {"column name": {"op": "value"}} (optional)

**Response**
- **Status:** [200]
- **Body:**  
  ```json
  {
    "count": 7
  }
  ```

**Errors**
- [400]: No lookup string provided 
- [402]: Insufficient Credits
- [500]: Error Processing request
- [404]: User/Table/db not found

---

