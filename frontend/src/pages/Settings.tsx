import { Button } from "@/components/ui/button";
import { API_URL } from "@/lib/api";

function SettingsPage() {

    const handleLogout = () => {
        fetch(API_URL+"/logout", {
            method: "POST",
            credentials: "include",
        })
        .then((response) => {
            if (response.ok) {
                console.log("User logged out");
            } else {
                console.error("Logout failed");
            }
        });

        // delete jwt cookie
        document.cookie = "jwt=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Lax; Secure";
    };

    const handleDeleteAccount = () => {
        fetch(API_URL+"/delete_account", {
            method: "POST",
            credentials: "include",
        })
        .then((response) => {
            if (response.ok) {
                console.log("User account deleted");
            } else {
                console.error("Account deletion failed");
            }
        });
    };

    return ( 
        <>
            <h1>Settings</h1>
            <Button onClick={handleLogout}>Log Out</Button>
            <Button onClick={handleDeleteAccount}>Delete Account</Button>
            <p>Deleting your account will delete all databases, tables, tokens, and other related data. this is permanent without confirmation!</p>
        </>
     );
}

export default SettingsPage;