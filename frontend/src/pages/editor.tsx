import { useMenuBar } from "@/components/menuContext";
import { Button } from "@/components/ui/button";
import { Popover, PopoverTrigger } from "@/components/ui/popover";
import { useEditorContext, Change } from "@/editorContext";
import { getTableData, getTableStructure } from "@/lib/api";
import { PopoverContent } from "@radix-ui/react-popover";
import { Plus, X } from "lucide-react";
import { t } from "node_modules/framer-motion/dist/types.d-CQt5spQA";
import { act, FocusEvent, ChangeEvent, JSXElementConstructor, Key, ReactElement, ReactNode, ReactPortal, use, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function TableEditor() {

    const { dbid } = useParams();
    const { selectedTable, setSelectedTable, selectedRows, setSelectedRows, changes, setChanges, data, setData, limit, offset, setTimetaken, setLimit, setOffset } = useEditorContext();


    const [structure, setStructure] = useState<any[]>([]);


    const [failedToGetData, setFailedToGetData] = useState(false);





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
    },[selectedTable, dbid]);


    useEffect(() => {
        const fetchTableData = async () => {
            if (selectedTable && dbid) {
                setFailedToGetData(false);
                getTableData(selectedTable, dbid, limit, offset).then((response) => {
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
    }, [selectedTable, dbid, limit, offset]); 


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

    if (newValue !== oldValue) {
        setChanges(prev => [
        ...prev,
        {
            rowId,
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
                                        <h4>Edit Column</h4>
                                        <Button variant='ghost' size='sm'><X  className="w-4 h-4"/></Button>
                                    </PopoverContent>
                                </Popover>
                                
                            </th>
                        ))}
                        
                    </tr>
                </thead>
                <tbody>
                {data.map((row, index) => (
                    <tr key={row.hiddenRowIDforFrontend !== undefined ? row.hiddenRowIDforFrontend : `${offset}-${index}`} className="border-t border-gray-300">
                        <td className="w-6 border border-gray-300 p-0.5 text-center">
                            <input checked={selectedRows.includes(row.hiddenRowIDforFrontend)} onChange={() => toggleRowSelection(row.hiddenRowIDforFrontend)} type="checkbox" className="w-3 h-3" />
                        </td>
                        {structure.map((column, colIndex) => ( 
                            <td key={column.name || colIndex} className="border border-gray-300 p-1">
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
                                    <input type={column.type} className="w-full p-0.5 text-xs" onBlur={(e) => handleInput(e, row.hiddenRowIDforFrontend, column.name, row[column.name])} defaultValue={row[column.name as keyof typeof row]} />
                                )}
                            </td>
                        ))}
                    </tr>
                ))}
                </tbody>
            </table>
            <div className="w-full bg-gray-100 h-15 sticky bottom-0">
                <textarea className="w-full h-15 p-2" placeholder="Filter for content..."></textarea>
            </div>
        </>
     );
}

export default TableEditor;