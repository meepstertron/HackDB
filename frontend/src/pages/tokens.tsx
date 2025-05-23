import { Button } from "@/components/ui/button";
import { ClipboardPaste, Shredder } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function TokenPage() {
    const navigate = useNavigate();

    const [tokens, setTokens] = useState([
        {
            id: "0000-0000-0000-0000", // excuse my fake uuid in prod itl be and actual one lol
            name: "some app",
            database: "some database",
            databaseid: "add85dce-9f03-4621-955b-3f48df098c48",
            createdAt: "2023-10-01",
            token: "hkdb_tkn_00000000-0000-0000-0000-00000000000"

        },
    ]);
    const handleRevoke = (id:string) => {
        // Logic to revoke the token
        console.log(`Revoking token with id: ${id}`);
    };

    return ( 
        <>
            <h1 className="text-2xl font-bold">Your Access tokens</h1>
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
                            <td className="px-4 py-2 border-gray-200 border">{token.database}</td>
                            <td className="px-4 py-2 border-gray-200 border">{token.createdAt}</td>
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