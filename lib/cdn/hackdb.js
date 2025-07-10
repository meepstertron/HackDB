class HackDB {
    constructor(token, baseUrl) {
        const tokenRegex = /^hkdb_tkn_[a-f0-9\-]{36}$/;
        this.token = token || null;
        this.baseUrl = baseUrl || 'https://hackdb.hexagonical.ch/api/sdk/v1';
        this.debug = false;
        this.connected = false;
        this._db_connection = this;
        this._tokenRegex = tokenRegex;

        return new Proxy(this, {
            get(target, prop, receiver) {
                if (prop in target) {
                    return Reflect.get(target, prop, receiver);
                }
                return new ModelProxy(prop, target._db_connection);
            }
        });
    }

    async connect() {
        if (!this.token) {
            console.error("No token provided. Please provide a valid HackDB token.");
            return false;
        }
        if (!this._tokenRegex.test(this.token)) {
            console.error("Invalid token format. Please provide a valid HackDB token.");
            return false;
        }
        try {
            const response = await fetch(`${this.baseUrl}/validatetoken`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            const data = await response.json();
            if (response.status === 200 && data.valid) {
                this.connected = true;
                console.log("Successfully connected to HackDB API.");
                return true;
            } else {
                this.connected = false;
                console.error("Failed to connect to HackDB API. Please check your token and base URL.");
                console.error("Response:", data);
                return false;
            }
        } catch (error) {
            this.connected = false;
            console.error("Network error:", error);
            return false;
        }
    }

    async get_credits() {
        if (!this.connected) {
            throw new Error("Not connected to HackDB API.");
        }
        const response = await fetch(`${this.baseUrl}/credits`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        const data = await response.json();
        return data.credits;
    }

    async get_tables() {
        if (!this.connected) {
            throw new Error("Not connected to HackDB API.");
        }
        const response = await fetch(`${this.baseUrl}/tables`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }
}

class ModelProxy {
    constructor(modelName, dbConnection) {
        this.modelName = modelName;
        this.dbConnection = dbConnection;
    }

    async create(data) {
        if (!this.dbConnection.connected) {
            throw new Error("Not connected to HackDB API.");
        }
        const response = await fetch(`${this.dbConnection.baseUrl}/tables/${this.modelName}/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.dbConnection.token}`
            },
            body: JSON.stringify({"data": JSON.stringify(data)})
        });
        return response.json();
    }

    async count(where = {}) {
        if (!this.dbConnection.connected) {
            throw new Error("Not connected to HackDB API.");
        }
        const params = new URLSearchParams();
        if (Object.keys(where).length > 0) {
            params.append('lookup_string', JSON.stringify(where));
        }
        const response = await fetch(`${this.dbConnection.baseUrl}/tables/${this.modelName}/count?${params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.dbConnection.token}`
            }
        });
        const data = await response.json();
        return data.count;
    }

    async find_many(where = {}, limit = 50) {
        if (!this.dbConnection.connected) {
            throw new Error("Not connected to HackDB API.");
        }
        const params = new URLSearchParams();
        if (Object.keys(where).length > 0) {
            params.append('lookup_string', JSON.stringify(where));
        }
        params.append('limit', limit);
        const response = await fetch(`${this.dbConnection.baseUrl}/tables/${this.modelName}/findmany?${params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.dbConnection.token}`
            }
        });
        return response.json();
    }

    async delete(where = {}) {
        if (!this.dbConnection.connected) {
            throw new Error("Not connected to HackDB API.");
        }
        const params = new URLSearchParams();
        if (Object.keys(where).length > 0) {
            params.append('lookup_string', JSON.stringify(where));
        }
        const response = await fetch(`${this.dbConnection.baseUrl}/tables/${this.modelName}/delete?${params.toString()}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.dbConnection.token}`
            }
        });
        return response.json();
    }
}