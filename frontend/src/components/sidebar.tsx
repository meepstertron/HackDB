import { Bug, Database, Hash, House, PercentDiamondIcon, Plus, Settings2, Table2, Workflow } from "lucide-react";
// use react router dom to navigate between pages
import { data, useNavigate, useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";



import { SidebarContent, SidebarFooter, SidebarGroup, SidebarHeader, Sidebar as SidebarUI } from "./ui/sidebar";
import { Button } from "./ui/button";
import { Tooltip } from "@radix-ui/react-tooltip";
import { TooltipContent, TooltipTrigger } from "./ui/tooltip";
import { ScrollArea } from "./ui/scroll-area";
import { Input } from "./ui/input";
import { cn } from "@/lib/utils";
import { getDatabaseTables } from "@/lib/api";
import { useEditorContext } from "@/editorContext";

function Sidebar() {
    const navigate = useNavigate();
    const elements = [
        { name: "Databases", icon: <Database />, location: "/databases", active: true },
        { name: "Workflows", icon: <Workflow />, location: "/workflows", active: false },
        { name: "Quota", icon: <PercentDiamondIcon />, location: "/quota", active: false },
        { name: "Tokens", icon: <Hash />, location: "/tokens", active: true },
        { name: "Settings", icon: <Settings2 />, location: "/settings", active: true },
    ];

    return ( 
        <aside className="w-16 h-full bg-white border-r border-gray-300 flex flex-col items-center p-4">
            
            <div className="mb-8">
                <img src="/logo192.png" alt="Logo" className="h-8 w-8" />
            </div>
            <ul className="flex flex-col items-center w-full text-gray-800">
                {elements.map((element) => (
                <li className={`flex flex-col items-center gap-1 py-2   w-16 ${!element.active ? "text-gray-500 cursor-auto" : "cursor-pointer hover:bg-gray-100"}`} onClick={ () => { if (element.active) { navigate(element.location) } } } key={element.name}>
                    {element.icon}
                    <span className="text-xs mt-1">{element.name}</span>
                </li>
                ))}
   
            </ul>
        </aside>
     );
}

export function SquareIconButton({ icon, label, onClick, className }: { 
    icon: React.ReactNode; 
    label: string; 
    onClick: () => void; 
    className?: string; 
}) {
    return (
        <Tooltip>
            <TooltipTrigger asChild>
                <Button variant="outline" className={cn("w-fit h-auto aspect-square", className)} onClick={onClick}>
                    {icon}
                </Button>
            </TooltipTrigger>
            <TooltipContent>
                <span>{label}</span>
            </TooltipContent>
        </Tooltip>
    );
}


function EditorSidebar() {

    // Remove unused navigate variable
    const navigate = useNavigate();
    const { dbid } = useParams();

    const { selectedTable, setSelectedTable, changes, tables, setTables } = useEditorContext();



    // make the 

    useEffect(() => {
        const fetchTables = async () => {
            if (!dbid) {
                setTables([]);
            } else {
                try {
                    let data = await getDatabaseTables(dbid);
                   setTables(data.tables);
                } catch (error) {
                    console.error("Error fetching tables:", error);
                    setTables([]);
                }
            }
        };

        fetchTables();
    }, [dbid]);



    


    return (
        <SidebarUI>
            <SidebarHeader>

            </SidebarHeader>
            <SidebarContent>
                <SidebarGroup>

                </SidebarGroup>
                <SidebarGroup>
                    <div className="flex gap-1">
                        <Input placeholder="Search tables..." />
                        <SquareIconButton icon={<Plus />} label="Add Table" onClick={() => {}} className="h-9" />
                    </div>
                    <ScrollArea>
                        {
                            tables && tables.length > 0 ? tables.map((table) => (
                                <Button key={table.id} variant="ghost" className={"w-full" + (selectedTable === table.id ? " bg-muted" : "")} onClick={() => { setSelectedTable(table.id); }}>
                                    <div className="flex flex-row gap-2 items-center justify-start w-full">
                                        <Table2 />
                                        <span>{table.name}</span>
                                    </div>
                                    <span className="text-xs text-muted-foreground font-normal">{table.rows}</span>
                                </Button>
                            )) : (
                                <div className="p-2 text-center text-muted-foreground">No tables found</div>
                            )
                        }
                    </ScrollArea>
                </SidebarGroup>
            </SidebarContent>
            <SidebarFooter>
                <div className="flex flex-row gap-1 items-start justify-start w-full">

                    <Tooltip>
                        <TooltipTrigger asChild><Button variant="outline" className="w-fit h-auto aspect-square"><House /></Button></TooltipTrigger>
                        <TooltipContent>
                            <span>Exit</span>
                        </TooltipContent>
                        
                    </Tooltip>
                    <Tooltip>
                        <TooltipTrigger asChild><Button variant="outline" className="w-fit h-auto aspect-square"><Bug /></Button></TooltipTrigger>
                        <TooltipContent>
                            <span>Report Issue</span>
                        </TooltipContent>
                        
                    </Tooltip>
                </div>
            </SidebarFooter>
        </SidebarUI>
    )
}




export default Sidebar;
export { EditorSidebar, Sidebar };