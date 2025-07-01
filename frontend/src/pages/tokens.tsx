import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { createToken, getUsersDatabases, getUserTokens, revokeToken } from "@/lib/api";
import { ClipboardPaste, Grid2x2Plus, Shredder } from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";


function TokenPage() {
    const [databases, setDatabases] = useState<Array<{name: string, id: string}>>([]); // This is just a placeholder, you can remove it if not needed

// [{name: "database", id: "uuid"}]



    useEffect(() => {
        getUserTokens().then((response) => {
            if (response && response.tokens) {
                setTokens(response.tokens);
            } else {
                console.error("Error fetching tokens:", response);
            }
        })

        getUsersDatabases().then((response) => {
            if (response && response.databases) {
                setDatabases(response.databases.map((db: {name: string, id: string}) => ({
                    name: db.name,
                    id: db.id
                })));
            } else {
                console.error("Error fetching databases:", response);
            }
        });
    }, []);

    const [tokens, setTokens] = useState([
        {
            id: "0000-0000-0000-0000", // excuse my fake uuid in prod itl be and actual one lol
            name: "some app",
            database: "some database",
            databaseid: "add85dce-9f03-4621-955b-3f48df098c48",
            created_at: "2023-10-01",
            token: "hkdb_tkn_00000000-0000-0000-0000-00000000000"

        },
    ]);
    const handleRevoke = (id:string) => {
        // Remove the very sigma token from the list
        setTokens(tokens.filter(token => token.id !== id));
        // uhhh no api route lol



        revokeToken(id).then((response) => {
            if (response && response.success) {
                console.log(`Token with id ${id} revoked`);
            }
        });
    };

    return (
        <>
            <div className="mb-4 flex justify-between items-center">
                <h1 className="text-2xl font-bold">Your Access tokens</h1>
                <Popover>
                    <PopoverTrigger asChild>
                        <Button variant="outline"><Grid2x2Plus />  Create Token</Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-80">
                        <div className="p-4">
                            <form onSubmit={(e) => {
                                e.preventDefault();
                                const formData = new FormData(e.target as HTMLFormElement);
                                const name = formData.get("name") as string;
                                const dbId = formData.get("database") as string;
                                createToken(name, dbId).then((response) => {

                                    if (response && response.token) {
                                        setTokens([...tokens, response.token]);
                                        toast.success("Token created successfully!");
                                        e.currentTarget.reset(); // Reset the form after successful creation
                                    } else {
                                        console.error("Error creating token:", response);
                                        toast.error("Failed to create token. Please try again.");
                                    }
                                });
                            }}>
                                <h3 className="font-bold">Create a new token</h3>
                                <p className="text-sm text-gray-600">Enter a name for your new token:</p>
                                <input type="text" className="border border-gray-300 rounded-md p-2 w-full" name="name" />
                                <p className="text-sm text-gray-600 mt-2">Select a database:</p>
                                <select name="database" className="border border-gray-300 rounded-md p-2 w-full">
                                    {databases.map((db) => (
                                        <option key={db.id} value={db.id}>{db.name}</option>
                                    ))}
                                </select>
                                <Button variant="outline" className="mt-2" type="submit">Create Token</Button>
                            </form>
                        </div>
                    </PopoverContent>
                </Popover>
            </div>
            <div
            className="p-3 mx-5 mb-4 outline-dashed outline-2 outline-yellow-500 bg-yellow-100 text-yellow-800 "
            >
                <h2 className="text-red-900 font-bold">Warning!</h2>
                Please treat these tokens like passwords. If someone gets access to them, they can access your database. I am not responsible if you accidentally leak them, make sure to always use .env files or other secure methods to store them. If you think your token has been compromised, please revoke it immediately. for more info check out the <a href="https://example.com" className="font-mono underline">documentation</a>
            </div>

            <table className="table-auto w-full">
                <thead>
                    <tr className="border-b border-gray-200">
                        <th>Name</th>
                        <th>Database</th>
                        <th>Created At</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {tokens.map((token) => (
                        <tr key={token.id} className="border-b border-gray-200">
                            <td className="px-4 py-2 border-gray-200 border">{token.name}</td>
                            <td className="px-4 py-2 border-gray-200 border"><a href={`/databases/${token.databaseid}`}>{token.database}</a></td>
                            <td className="px-4 py-2 border-gray-200 border">{token.created_at}</td>
                            <td className="px-4 py-2 border-gray-200 border">
                                <div className="flex space-x-2">
                                    <Button variant="outline" className="w-1/2" onClick={() => handleRevoke(token.id)}><Shredder /> Revoke</Button>
                                    <Button variant="outline" className="w-1/2" onClick={() => navigator.clipboard.writeText(token.token)}><ClipboardPaste /> Copy</Button>
                                </div>
                            </td>
                        </tr>
                    ))}
                </tbody>

            </table>
        </>
     );
}

export default TokenPage;