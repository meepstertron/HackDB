import { createContext, useContext, useState } from 'react';
import React from 'react';


export type Change = {
    uuid: string;
    table: string;
    type: string;
    payload: any;
    timestamp: string;
    undo: () => void;
}


type EditorContextType = {
    selectedTable: string | null;
    setSelectedTable: (table: string | null) => void;
    changes: Change[];
    setChanges: (changes: any[] | ((prev: any[]) => any[])) => void;
    tables: Array<{id: string, name: string, rows: number}>;
    setTables: (tables: Array<{id: string, name: string, rows: number}>) => void;
    selectedRows: number[];
    setSelectedRows: (rows: number[]) => void;
    limit: number;
    setLimit: (limit: number) => void;
    offset: number;
    setOffset: (offset: number) => void;
    data: any[];
    setData: (data: any[] | ((prev: any[]) => any[])) => void;
    timetaken : number;
    setTimetaken: (timetaken: number) => void;
    contentFilter?: string;
    setContentFilter?: (filter: string) => void;
}

const EditorContext = createContext<EditorContextType | undefined>(undefined);

export const EditorProvider = ({ children }: { children: React.ReactNode }) => {
    const [selectedTable, setSelectedTable] = useState<string | null>(null);
    const [tables, setTables] = React.useState<Array<{id: string, name: string, rows: number}>>([
            { id: "1", name: "Items", rows: 10}
        ]);
    const [selectedRows, setSelectedRows] = useState<number[]>([]);

    const [changes, setChanges] = useState<any[]>([]);
    const [limit, setLimit] = useState<number>(50);
    const [offset, setOffset] = useState<number>(0);
    const [data, setData] = useState<any[]>([]);
    const [timetaken, setTimetaken] = useState<number>(0);
    const [contentFilter, setContentFilter] = useState<string>('');

    let hasDismissedLimitAlert = false;
    if (limit > 1000 && !hasDismissedLimitAlert) {
        hasDismissedLimitAlert = confirm("Warning: Fetching more than 1,000 rows may cause lag, sadness, and browser-based suffering. Are you sure what you are doing is worth it?");
        if (!hasDismissedLimitAlert) {
            setLimit(50);
        }
    }

    return (
        <EditorContext.Provider value={{ selectedTable, setSelectedTable, changes, setChanges, tables, setTables, selectedRows, setSelectedRows, limit, setLimit, offset, setOffset, data, setData, timetaken, setTimetaken, contentFilter, setContentFilter }}>
            {children}
        </EditorContext.Provider>
    )
}


export const useEditorContext = () => {
    const context = useContext(EditorContext);
    if (!context) {
        throw new Error("useEditorContext must be used within an EditorProvider");
    }
    return context;
}

