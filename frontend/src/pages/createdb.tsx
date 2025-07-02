import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { createDatabase } from "@/lib/api";
import { useState } from "react";


import { useNavigate } from "react-router-dom";

function DatabaseCreationPage() {

    const navigate = useNavigate();


    const [dbName, setDbName] = useState("");

    const handleCreateDatabase = (name: string) => {
        createDatabase(name)
            .then((data) => {
                console.log("Database created successfully:", data);
                navigate(`/databases/${data.database_id}`);
            })
            .catch((error) => {
                console.error("Error creating database:", error);
            });
    }

    return (
        <div>
            <h1 className="text-2xl mb-2">Create Database</h1>
            <p className="mb-4 text-muted-foreground">
                Please enter a name for your new database. The name must be unique and can only contain alphanumeric characters, underscores, and hyphens. you may only have one database of this name per account.
            </p>
            <Input placeholder="Database Name" value={dbName} onChange={(e) => setDbName(e.target.value)} />

            <Button variant="default" className="mb-4" onClick={() => handleCreateDatabase(dbName)} disabled={!dbName}>
                Create New Database
            </Button>
        </div>
    );
}

export default DatabaseCreationPage;