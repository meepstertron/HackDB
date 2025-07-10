import { useMenuBar } from "@/components/menuContext";
import { Button } from "@/components/ui/button";
import { getDatabaseInfo } from "@/lib/api";
import { Pencil } from "lucide-react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function DBInfo() {

    const { setMenuItems, setTitle } = useMenuBar();

    const id = useParams().id;

    
    

    const [properties, setProperties] = useState([
        { name: "UUID", value: id },
        { name: "Database Name", value: "Loading...", editable: true, onEdit: (value:string) => {
            setProperties(prevProperties => prevProperties.map(prop => 
                prop.name === "Database Name" ? { ...prop, value } : prop
            ));
        } },

        { name: "Created At", value: "Loading...", editable: false, onEdit: () => {} },
        { name: "Last Updated", value: "Loading...", editable: false, onEdit: () => {} },
        { name: "number of Tables", value: "Loading...", editable: false, onEdit: () => {} },
        { name: "Quota Usage / Week", value: "Loading...", editable: false, onEdit: () => {} }
    ]);

    const [tables, setTables] = useState([
        { name: "Loading...", rows: "Loading...", size: "Loading...", lastModified: "Loading..." }
    ]);

    useEffect(() => {

        const fetchData = async () => {
            const response = await getDatabaseInfo(String(id));
            if (response && response.database) {
                const dbInfo = response.database;
                    setProperties([
                        { name: "UUID", value: dbInfo.database_id, editable: false, onEdit: () => {} },
                        { 
                            name: "Database Name", 
                            value: dbInfo.name, 
                            editable: true, 
                            onEdit: (newValue: string) => {
                                setProperties(prevProperties => prevProperties.map(prop => 
                                    prop.name === "Database Name" ? { ...prop, value: newValue } : prop
                                ));
                                // TODO: Add API call to update database name on the backend
                                setTitle("HackDB - " + newValue); // Use newValue here
                            } 
                        },
                        { name: "Created At", value: dbInfo.created_at, editable: false, onEdit: () => {} },

                        { name: "number of Tables", value: dbInfo.num_tables, editable: false, onEdit: () => {} },
                        { name: "Quota Usage / Week", value: dbInfo.quota_usage ?? "N/A", editable: false, onEdit: () => {} }
                    ]);
                setTitle("HackDB - " + dbInfo.name);
                setTables(dbInfo.tables);
            } else {
                console.error("Failed to fetch database info or data is not in expected format");
                setProperties(prevProperties => prevProperties.map(prop => 
                    prop.value === "Loading..." ? { ...prop, value: "Error loading data" } : prop
                ));
            }
        };
        
        fetchData();
        
    }, [id]);

    return (
        <>
            <Button variant={"outline"} className="mb-4" onClick={() => window.location.href = "/editor/" + id}>
                <Pencil className="mr-2" /> Open in Editor
            </Button>
            <table className="rounded table table-striped table-bordered border-colapse border border-gray-400">
                
                <tbody className="text-center rounded">
{properties.map((property, index) => (
                    <tr key={index}>
                        <td className="border border-gray-400 p-1">{property.name}</td>
                        {property.editable ? (
                            <td className="border border-gray-400 p-1">
                                <input 
                                    type="text" 
                                    value={property.value} 
                                    onChange={(e) => property.onEdit(e.target.value)} 
                                    className="w-full p-1"
                                />
                            </td>
                        ) : (
                            <td className="border border-gray-400 p-1">{property.value}</td>
                        )}
                    </tr>))}
                </tbody>
            </table>
            <table className="mt-4 rounded table table-striped table-bordered border-colapse border border-gray-400">
                <tbody className="text-center rounded">
                    <tr className="bg-gray-200">
                        <td className="border border-gray-400 p-1">
                            Table Name
                        </td>
                        <td className="border border-gray-400 p-1">
                            Number of Rows
                        </td>
                        <td className="border border-gray-400 p-1">
                            File Size
                        </td>
                        


                    </tr>
                
                    
                        {/* <td className="border border-gray-400 p-1">Example Table</td>
                        <td className="border border-gray-400 p-1">100</td>
                        <td className="border border-gray-400 p-1">1 MB</td>
                        <td className="border border-gray-400 p-1">2023-10-01</td>
                        <td className="border border-gray-400 p-1">
                            <Button variant="outline" className="flex items-center">
                                <Pencil className="mr-2" /> Edit
                            </Button>
                        </td> */}
                        {tables.map((table, index) => (
                            <tr key={index}>
                                <td className="border border-gray-400 p-1">{table.name}</td>
                                <td className="border border-gray-400 p-1">{table.rows}</td>
                                <td className="border border-gray-400 p-1">{table.size}</td>

                            </tr>))}
                        

                    
                </tbody>
            </table>
        </>
    );
}

export default DBInfo;