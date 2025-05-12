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
