import { useMenuBar } from "@/components/menuContext";
import { useEditorContext } from "@/editorContext";
import { getTableStructure } from "@/lib/api";
import { act, use, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function TableEditor() {

    const { dbid } = useParams();
    const { selectedTable, setSelectedTable } = useEditorContext();


    const [structure, setStructure] = useState<any[]>([]);



    let data = [
        {
            id: 1,
            name: "John Doe",
            role: "admin"
        },
        {
            id: 2,
            name: "Jane Smith",
            role: "user"
        },
        {
            id: 3,
            name: "Alice Johnson",
            role: "guest"
        }
    ];




    type Change = {
        column: string;
        type: "add" | "remove" | "modify";
        value: any;
        previousValue?: any;
    }

    let changes: Change[] = [];


    function handleChange(column: string, type: "add" | "remove" | "modify", value: any, previousValue?: any) {
        changes.push({ column, type, value, previousValue });
        console.log(changes);
    }


    useEffect(() => {
        const fetchTableStructure = async () => {
            console.log("precheck")
            if (selectedTable && dbid) {
                console.log("Fetching table structure for table: " + selectedTable);
                setStructure(await getTableStructure(selectedTable, dbid));
            }
        }
        fetchTableStructure();
    },[selectedTable, dbid]);

    if (!selectedTable) {
        return (
            <div className="flex items-center justify-center h-full">
                <h1 className="text-2xl font-bold">Select a table to edit</h1>
            </div>
        );
    }

    return (

        <>
            <table className="border-collapse text-sm border border-gray-300">
                <thead>
                    <tr>
                        <th className="w-6 h-6 border border-gray-300 p-0.5 text-center">
                            <input type="checkbox" className="w-3 h-3" />
                        </th>
                        {structure.map((column, index) => (
                            <th className="text-left border border-gray-300 p-1" key={index}>
                                {column.name} <span className="text-xs font-normal">{column.type}</span>
                            </th>
                        ))}
                        
                    </tr>
                </thead>
                <tbody>
                {data.map((row, index) => (
                    <tr key={index} className="border-t border-gray-300">
                        <td className="w-6 border border-gray-300 p-0.5 text-center">
                            <input type="checkbox" className="w-3 h-3" />
                        </td>
                        {structure.map((column, index) => (
                            <td key={index} className="border border-gray-300 p-1">
                                {column.type === "select" ? (
                                    <select className="w-full bg-gray-100 text-xs rounded" defaultValue={String(row[column.name as keyof typeof row])}>
                                        {column.options?.map((option, index) => (
                                            <option value={option.value} key={index}>{option.label}</option>
                                        ))}
                                    </select>
                                ) : (
                                    <input type={column.type} className="w-full p-0.5 text-xs" defaultValue={row[column.name as keyof typeof row]} />
                                )}
                            </td>
                        ))}
                    </tr>
                ))}
                </tbody>
            </table>
        </>
     );
}

export default TableEditor;