

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

function getMyself() {
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