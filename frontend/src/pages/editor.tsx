import { useMenuBar } from "@/components/menuContext";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Popover, PopoverTrigger, PopoverContent} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useEditorContext, Change } from "@/editorContext";
import { getTableData, getTableStructure } from "@/lib/api";

import { ArrowDownWideNarrow, ArrowUpWideNarrow, Plus, Save, Trash2, X } from "lucide-react";
import { t } from "node_modules/framer-motion/dist/types.d-CQt5spQA";
import { act, FocusEvent, ChangeEvent, JSXElementConstructor, Key, ReactElement, ReactNode, ReactPortal, use, useEffect, useState } from "react";
import { useParams } from "react-router-dom";


const datatypes = [ // postgresql datatypes
    "text",
    "integer",
    "float",
    "double",
    "boolean",
    "cidir",
    "date",
    "timestamp",
    "json"
]


export const constructWhereClause = (row: any ) => { //give whole row as input!!
        let where: { [key: string]: any } = {};
        for (const key in row) {
            let value = row[key];


            if (key === "hiddenRowIDforFrontend") continue; // Skip the frontend ID


            if (value instanceof Date) {
                value = value.toISOString().slice(0, 19).replace('T', ' '); // Convert Date to SQL format
            }



            if (value !== null && value !== undefined) {
                where[key] = {"equals": value };
            }
        }
        return where;
    };


function TableEditor() {

    const { dbid } = useParams();
    const { selectedTable, setSelectedTable, selectedRows, setSelectedRows, changes, setChanges, data, setData, limit, offset, setTimetaken, setLimit, setOffset, contentFilter, setContentFilter, sortBy, setSortBy, addingNewColumn, setAddingNewColumn, refreshKey, setRefreshKey, failedToGetData, setFailedToGetData } = useEditorContext();


    const [structure, setStructure] = useState<any[]>([]);
    const [newRow, setNewRow] = useState<any>({});


    



    useEffect(() => {
        if (setContentFilter) {
            setContentFilter(`{}`);
        }
    }, []);


    useEffect(() => {
        const fetchTableStructure = async () => {
            console.log("precheck")
            if (selectedTable && dbid) {
                setLimit(50);
                setOffset(0);
                console.log("Fetching table structure for table: " + selectedTable);
                setStructure(await getTableStructure(selectedTable, dbid));
                

            }
        }
        fetchTableStructure();
    },[selectedTable, dbid, refreshKey ]);


    useEffect(() => {
        const fetchTableData = async () => {
            if (selectedTable && dbid) {
                setFailedToGetData(false);
                let sortbystr = (sortBy && sortBy.column) ? `${sortBy.column},${sortBy.direction}` : undefined;

                getTableData(selectedTable, dbid, limit, offset, sortbystr).then((response) => {
                    if (response && response.data) {
                        const processedData = response.data.map((item: any, index: number) => ({
                            ...item,
                            hiddenRowIDforFrontend: (index * 1.4375) + offset 
                        }));
                        
                        setData(processedData);
                        setTimetaken(response.time);
                    } else {
                        console.error("Error fetching table data:", response);
                        setData([]);
                        setFailedToGetData(true);
                    }
                });
            }
        }
        fetchTableData();
    }, [selectedTable, dbid, limit, offset, sortBy, refreshKey]); 




    const toggleRowSelection = (rowId: number) => {
        const newSelectedRows = selectedRows.includes(rowId) 
            ? selectedRows.filter((id) => id !== rowId) 
            : [...selectedRows, rowId];
        setSelectedRows(newSelectedRows);
    };


    const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
        const checked = e.target.checked;
        if (checked) {
            const allRowIds = data.map((row) => row.hiddenRowIDforFrontend);
            setSelectedRows(allRowIds);
        } else {
            setSelectedRows([]);
        }
    };


    const handleInput = (
    e: FocusEvent<HTMLInputElement | HTMLSelectElement> | ChangeEvent<HTMLInputElement>,
    rowId: number,
    column: string,
    oldValue: any
    ) => {
    const target = e.target as HTMLInputElement | HTMLSelectElement;
    let newValue: any;

    if (target instanceof HTMLInputElement && target.type === 'checkbox') {
        newValue = target.checked;
    } else {
        newValue = target.value;
    }

    if (target.type === 'datetime-local') {
        newValue = turnNormaliedTimestampBackIntoNormalSQLTimestamp(newValue);
    }
    if (oldValue == newValue) {
        return; // No change, do nothing
    }

    if (target.type === 'integer' || target.type === 'number') {
        newValue = parseInt(newValue, 10);
    }
    if (target.type === 'float' || target.type === 'double') {
        newValue = parseFloat(newValue);
    }
    const currentRow = data.find(row => row.hiddenRowIDforFrontend === rowId);
    const where = currentRow ? constructWhereClause(currentRow) : {};

    // remove the edited value from the where clause since it wont be the same as the old value
    if (where[column]) {
        delete where[column];
        
    }
    delete where.hiddenRowIDforFrontend;

    if (newValue !== oldValue) {
        setChanges(prev => [
        ...prev,
        {
            where: where,
            column,
            oldValue,
            newValue,
            table: selectedTable,
            type: "edit",
            timestamp: new Date().toISOString(),
        },
        ]);
        setData(prev =>
        prev.map((row) =>
            row.hiddenRowIDforFrontend === rowId
            ? { ...row, [column]: newValue }
            : row


        )
        );
    }
    };



    // this is needed because html is kinda freaky ahh 
    function normalizeTimestampForInput(value: any) {
        if (!value) return '';
        
        if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(value)) {
            return value.slice(0, 16);
        }
        
        const date = new Date(value);
        if (!isNaN(date.getTime())) {
            
            const pad = (n: number) => n.toString().padStart(2, '0');
            const yyyy = date.getFullYear();
            const mm = pad(date.getMonth() + 1);
            const dd = pad(date.getDate());
            const hh = pad(date.getHours());
            const min = pad(date.getMinutes());
            return `${yyyy}-${mm}-${dd}T${hh}:${min}`;
        }
        return '';
    }


    function turnNormaliedTimestampBackIntoNormalSQLTimestamp(value: string) {
        if (!value) return null;
        const date = new Date(value);
        if (isNaN(date.getTime())) return null; // Invalid date
        return date.toISOString().slice(0, 19).replace('T', ' '); // Format as 'YYYY-MM-DD HH:MM:SS'
    }


    if (!selectedTable) {
        return (
            <div className="flex items-center justify-center h-full">
                <h1 className="text-2xl font-bold">Select a table to edit</h1>
            </div>
        );
    }

    if (failedToGetData) {
        return (
            <div className="flex items-center justify-center h-full">
                <h1 className="text-2xl font-bold">No Records Found with these parameters</h1>
            </div>
        );
    }
    return (

        <>
            <table className="border-collapse text-sm border border-gray-300">
                <thead>
                    <tr>
                        <th className="w-6 h-6 border border-gray-300 p-0.5 text-center">
                            <input type="checkbox" className="w-3 h-3" onChange={handleSelectAll} />
                        </th>
                        {structure.map((column, index) => (
                            <th className="text-left border border-gray-300 p-1 hover:bg-gray-50 cursor-pointer" key={column.name || index}>
                                <Popover>
                                    <PopoverTrigger className="flex items-center w-full">
                                        {column.name} <span className="text-xs font-normal ml-2">{column.type}</span>
                                    </PopoverTrigger>
                                    <PopoverContent>
                                        <h4 className="text-lg mb-2">Edit Column</h4>

                                        <Button variant='ghost' size='sm' className="" onClick={() => {
                                            setSortBy({
                                                column: column.name,
                                                direction: sortBy?.column === column.name && sortBy?.direction === 'asc' ? 'desc' : 'asc'
                                            });
                                            

                                        }}>{sortBy?.column === column.name && sortBy?.direction === 'asc' ? <ArrowDownWideNarrow className="w-4 h-4" /> : <ArrowUpWideNarrow className="w-4 h-4" />}</Button>
                                        <Button variant='ghost' size='sm' className="ml-2" onClick={() => {
                                            setStructure(prev => prev.filter((_, i) => i !== index));
                                            setChanges(prev => [
                                                ...prev,
                                                {
                                                    column: column.name,
                                                    oldValue: null,
                                                    newValue: null,
                                                    table: selectedTable,
                                                    type: "delete_column",
                                                    timestamp: new Date().toISOString(),
                                                },
                                            ]);
                                        }}><Trash2 className="w-4 h-4" /></Button>

                                        <Label htmlFor="column-name" className="mb-1 mt-2">Column Name</Label>
                                        <Input id="column-name" defaultValue={column.name} />
                                        <Label htmlFor="column-type" className="mt-2 mb-1">Column Type</Label>
                                        <Select>
                                            <SelectTrigger id="column-type" className="w-full">
                                                <SelectValue placeholder="Select a type" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {datatypes.map((type) => (
                                                    <SelectItem key={type} value={type}>
                                                        {type}
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                        <Label htmlFor="default-value" className="mt-2 mb-1">Default Value</Label>
                                        
                                        
                                        <Input id="default-value" defaultValue={column.defaultValue || ''} placeholder="Optional default value" />

                                        <div className="flex items-center space-x-2">
                                            
                                            <Checkbox id="allow-nullvalues" />
                                            <Label htmlFor="allow-nullvalues" className="mt-2 mb-1">Allow Null Values</Label>
                                        </div>


                                        <div className="flex items-center space-x-2">
                                            
                                            <Checkbox id="Primary Key" checked={column.primaryKey || false} onChange={(e) => {
                                                setStructure(prev => {
                                                    const newStructure = [...prev];
                                                    newStructure[index] = {
                                                        ...newStructure[index],
                                                        primaryKey: (e.target as HTMLInputElement).checked,
                                                    };
                                                    return newStructure;
                                                });
                                                setChanges(prev => [
                                                    ...prev,
                                                    {
                                                        column: column.name,
                                                        oldValue: column.primaryKey || false,
                                                        newValue: (e.target as HTMLInputElement).checked,
                                                        table: selectedTable,
                                                        type: "edit",
                                                        timestamp: new Date().toISOString(),
                                                    },
                                                ]);
                                            }
                                            } />
                                            <Label htmlFor="Primary Key" className="mt-2 mb-1">Primary Key</Label>
                                        </div>
                                        <Button variant="default"><Save /> Save Changes</Button>

                                    </PopoverContent>
                                </Popover>
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                {addingNewColumn && (
                    <tr className="border-t border-gray-300">
                        <td className="w-6 border border-gray-300 p-0.5 text-center">
                            <input type="checkbox" className="w-3 h-3" />
                        </td>
                        {structure.map((column, colIndex) => (
                            <td key={column.name || colIndex} className="border border-gray-300 ">
                                <Popover>
                                    <PopoverTrigger className="p-0 ">
                                        <div className="w-full h-full bg-muted cursor-pointer p-1 min-h-[24px]">
                                            {column.default ? "DEFAULT" : column.nullable ? "NULL" : "!EMPTY!"} 
                                        </div>
                                    </PopoverTrigger>
                                    <PopoverContent className="p-0 min-w-fit w-100">
                                        <div className="p-0">
                                            <textarea className="w-full h-full p-1 min-h-[24px] resize-none" placeholder="Content Goes here"></textarea>
                                            <hr className="my-1 border-dashed border-gray-300" />
                                            <div className="flex items-center justify-between p-1">
                                                <div>
                                                    <Button size="sm" variant="outline" onClick={() => setNewRow({ ...newRow, [column.name]: null })}>
                                                        Set NULL
                                                    </Button>

                                                    {column.default ? <Button size="sm" variant="outline" onClick={() => setNewRow({ ...newRow, [column.name]: column.defaultValue ?? "" })}>
                                                        Set Default
                                                    </Button> : null}
                                                </div><div >
                                                    <Button size="sm" variant="outline">
                                                        Cancel
                                                    </Button>
                                                    <Button size="sm" variant="default">
                                                        Submit
                                                    </Button>
                                                </div>
                                            </div>
                                        </div>
                                    </PopoverContent>
                                </Popover>
                            </td>
                        ))}
                    </tr>
                )}
                {data.map((row, index) => (
                    <tr key={row.hiddenRowIDforFrontend !== undefined ? row.hiddenRowIDforFrontend : `${offset}-${index}`} className="border-t border-gray-300">
                        <td className="w-6 border border-gray-300 p-0.5 text-center">
                            <input checked={selectedRows.includes(row.hiddenRowIDforFrontend)} onChange={() => toggleRowSelection(row.hiddenRowIDforFrontend)} type="checkbox" className="w-3 h-3" />
                        </td>
                        {structure.map((column, colIndex) => (
                            <td
                                key={column.name || colIndex}
                                className={
                                    "border border-gray-300 p-1" +
                                    (!column.nullable && (row[column.name as keyof typeof row] === null || row[column.name as keyof typeof row] === undefined)
                                        ? " bg-red-400"
                                        : "")
                                }
                            >
                                {column.type === "select" ? (
                                    <select className="w-full bg-gray-100 text-xs rounded" defaultValue={String(row[column.name as keyof typeof row])} onBlur={(e) => handleInput(e, row.hiddenRowIDforFrontend, column.name, row[column.name])}>
                                        {column.options?.map((option: { value: string | number | readonly string[] | undefined; label: string | number | bigint | boolean | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<string | number | bigint | boolean | ReactPortal | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | null | undefined> | null | undefined; }, index: Key | null | undefined) => (
                                            <option value={option.value} key={index}>{option.label}</option>
                                        ))}
                                    </select>
                                ) : column.type.includes("timestamp") ? (
                                    <input
                                        type="datetime-local"
                                        className="w-full p-0.5 text-xs"
                                        onBlur={(e) => handleInput(e, row.hiddenRowIDforFrontend, column.name, row[column.name])}
                                        defaultValue={normalizeTimestampForInput(row[column.name as keyof typeof row])}
                                    />
                                ) : column.type === "boolean" ? (
                                    <input type="checkbox" className="w-full p-0.5 text-xs" onChange={(e) => handleInput(e, row.hiddenRowIDforFrontend, column.name, row[column.name])} checked={row[column.name as keyof typeof row]} />
                                ) : (
                                    <input type={column.type} className="w-full p-0.5 text-xs" onBlur={(e) => handleInput(e, row.hiddenRowIDforFrontend, column.name, row[column.name])} defaultValue={JSON.stringify(row[column.name as keyof typeof row])} />
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