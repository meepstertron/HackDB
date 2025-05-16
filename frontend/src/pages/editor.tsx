import { useMenuBar } from "@/components/menuContext";
import { useEditorContext } from "@/editorContext";
import { getTableStructure } from "@/lib/api";
import { randomBytes } from "crypto";
import { act, JSXElementConstructor, Key, ReactElement, ReactNode, ReactPortal, use, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function TableEditor() {

    const { dbid } = useParams();
    const { selectedTable, setSelectedTable, selectedRows, setSelectedRows, changes, setChanges } = useEditorContext();


    const [structure, setStructure] = useState<any[]>([]);





    const [data, setData] = useState(() => [
        {
            hiddenRowIDforFrontend: Math.floor(Math.random() * 1000000),
            id: 1,
            name: "John Doe",
            role: "admin"
        },
        {
            hiddenRowIDforFrontend: Math.floor(Math.random() * 1000000),
            id: 2,
            name: "Jane Smith",
            role: "user"
        },
        {
            hiddenRowIDforFrontend: Math.floor(Math.random() * 1000000),
            id: 3,
            name: "Alice Johnson",
            role: "guest"
        }
    ]);



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

    const toggleRowSelection = (rowId: number) => {
        const newSelectedRows = selectedRows.includes(rowId) 
            ? selectedRows.filter((id) => id !== rowId) 
            : [...selectedRows, rowId];
        setSelectedRows(newSelectedRows);
    };


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
                            <input checked={selectedRows.includes(row.hiddenRowIDforFrontend)} onChange={() => toggleRowSelection(row.hiddenRowIDforFrontend)} type="checkbox" className="w-3 h-3" />
                        </td>
                        {structure.map((column, index) => (
                            <td key={index} className="border border-gray-300 p-1">
                                {column.type === "select" ? (
                                    <select className="w-full bg-gray-100 text-xs rounded" defaultValue={String(row[column.name as keyof typeof row])}>
                                        {column.options?.map((option: { value: string | number | readonly string[] | undefined; label: string | number | bigint | boolean | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<string | number | bigint | boolean | ReactPortal | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | null | undefined> | null | undefined; }, index: Key | null | undefined) => (
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