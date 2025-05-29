import { json } from "stream/consumers";

export const API_URL = import.meta.env.VITE_API_URL || 'https://condor-willing-buck.ngrok-free.app/api';


interface Database {
    id: string;
    name: string;
    tables: number;
}


export function getMyself() {
        fetch(API_URL + "/me", {
        method: "GET",
        credentials: "include"})
        .then(async (response) => {
            if (response.status === 200) {
                const jsonData = await response.json()
                return {
                    valid: jsonData.valid || false,
                    username: jsonData.username || null,
                    email: jsonData.email || null,
                    slack_id: jsonData.slack_id || null
                }
            } else {
                throw new Error("Failed to fetch user data")
            }
        })
}


export function getUsersDatabases() {
    return fetch(API_URL + "/userdbs", {
        method: "GET",
        credentials: "include"})
        .then(async (response) => {
            if (response.status === 200) {
                const jsonData = await response.json()
                return jsonData
            } else {
                throw new Error("Failed to fetch user data")
            }
        })
        .catch((error) => {
            console.error("Error fetching user data:", error)
            return []
        });
}


export function getDatabaseInfo(db_id: string) {
    return fetch(API_URL + "/userdbs/" + db_id, {
        method: "GET",
        credentials: "include"})
        .then (async (response) => {
            if (response.status === 200) {
                const jsonData = await response.json()
                return jsonData
            } else {
                throw new Error("Failed to fetch user data")
            }
        })
        .catch((error) => {
            console.error("Error fetching database info:", error)
            return null
        });
}


export function getDatabaseTables(db_id: string) {
    return fetch(API_URL + "/userdbs/" + db_id + "/tables?type=lite", {
        method: "GET",
        credentials: "include"})
        .then (async (response) => {
            if (response.status === 200) {
                const jsonData = await response.json()
                return jsonData
            } else {
                throw new Error("Failed to fetch user data")
            }
        })
        .catch((error) => {
            console.error("Error fetching database info:", error)
            return null
        });
}

export function getTableStructure(table_id: string, db_id: string) {
    return fetch(API_URL + "/userdbs/"+db_id+ "/tables?type=struct&tableid="+table_id, {
        method: "GET",
        credentials: "include"
    })
        .then (async (response) => {
            if (response.status === 200) {
                const jsonData = await response.json()
                return jsonData
            } else {
                throw new Error("Failed to fetch user data")
            }
        })
        .catch((error) => {
            console.error("Error fetching database info:", error)
            return null
        });
}

export function getTableData(table_id: string, db_id: string, limit: number, offset: number) {


    return fetch(API_URL + "/userdbs/"+db_id+ "/tables?type=data&tableid="+table_id+"&limit="+limit+"&offset="+offset, {
        method: "GET",
        credentials: "include"
    })
        .then (async (response) => {
            const end = performance.now();
            

            if (response.status === 200) {
                const jsonData = await response.json()
                return { data: jsonData.rows, time: jsonData.time_taken }
            } else {
                throw new Error("Failed to fetch user data")
            }
        })
        .catch((error) => {
            console.error("Error fetching database info:", error)
            return null
        });
}


export function getUserTokens() {
    return fetch(API_URL + "/userdbs/tokens", {
        method: "GET",
        credentials: "include"
    })
        .then (async (response) => {
            if (response.status === 200) {
                const jsonData = await response.json()
                return jsonData
            } else {
                throw new Error("Failed to fetch user tokens")
            }
        })
        .catch((error) => {
            console.error("Error fetching user tokens:", error)
            return null
        });
}


export function commitChanges(changes: any[], db_id: string) {
    return fetch(API_URL + "/userdbs/" + db_id + "/commit", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ commits:changes })
    })
        .then(async (response) => {
            if (response.status === 200) {
                const jsonData = await response.json()
                return jsonData
            } else {
                throw new Error("Failed to commit changes")
            }
        })
        .catch((error) => {
            console.error("Error committing changes:", error)
            return null
        });
}