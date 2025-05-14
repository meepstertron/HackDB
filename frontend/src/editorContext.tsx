import { createContext, useContext, useState } from 'react';

type EditorContextType = {
    selectedTable: string | null;
    setSelectedTable: (table: string | null) => void;
}

const EditorContext = createContext<EditorContextType | undefined>(undefined);

export const EditorProvider = ({ children }: { children: React.ReactNode }) => {
    const [selectedTable, setSelectedTable] = useState<string | null>(null);

    return (
        <EditorContext.Provider value={{ selectedTable, setSelectedTable }}>
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