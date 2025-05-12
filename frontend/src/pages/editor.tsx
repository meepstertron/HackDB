import { useMenuBar } from "@/components/menuContext";
import { useEffect, useState } from "react";

function TableEditor() {

    const { setMenuItems, setTitle } = useMenuBar();
    let structure = [
        {
            name: "id",
            type: "int",
            primary: true,
            autoIncrement: true,
            nullable: false,
            default: null,
            unique: true,
            
        },
        {
            name: "name",
            type: "text",
            primary: false,
            autoIncrement: false,
            nullable: false,
            default: null,
            unique: false
        },
        {
            name: "role",
            type: "select",
            primary: false,
            autoIncrement: false,
            nullable: false,
            default: null,
            unique: false,
            options: [
                { value: "admin", label: "Admin" },
                { value: "user", label: "User" },
                { value: "guest", label: "Guest" }
            ]
        }
    ];
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
    let tableName = "Table Name";

    useEffect(() => {
        setTitle("Editor - "+ tableName);
        setMenuItems([
            {
                name: "Database",
            },
            {
                name: "Table",
                items:[
                    {
                        name: "Add Row",

                    },
                    {
                        name: "Drop table",
                    }
                ]
            }
        ]);
    }, []);

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

    function handleNewColumn() {

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