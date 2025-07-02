import { Bug, Check, Copy, Database, Edit, Hash, House, PercentDiamondIcon, Plus, ScissorsLineDashed, Settings2, Table2, Trash2, Workflow } from "lucide-react";
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
import { createTable, getDatabaseTables, getUsersDatabases, tableAction } from "@/lib/api";
import { useEditorContext } from "@/editorContext";
import { DBSwitcher } from "./dbswitcher";
import { ContextMenu, ContextMenuContent, ContextMenuItem, ContextMenuSub, ContextMenuSubContent, ContextMenuSubTrigger, ContextMenuTrigger } from "./ui/context-menu";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";

function Sidebar() {
    const navigate = useNavigate();
    const elements = [
        { name: "Databases", icon: <Database />, location: "/databases", active: true },
        { name: "Workflows", icon: <Workflow />, location: "/workflows", active: false },
        { name: "Quota", icon: <PercentDiamondIcon />, location: "/quota", active: true },
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
    onClick?: () => void; 
    className?: string; 
}) {
    return (
        <Tooltip>
            <TooltipTrigger asChild>
                <Button type="button" variant="outline" className={cn("w-fit h-auto aspect-square dark:text-white", className)} onClick={onClick}>
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
    const [newTableName, setNewTableName] = useState("");

    const { selectedTable, setSelectedTable, changes, tables, setTables, databases, setDatabases, setRefreshKey, refreshKey } = useEditorContext();



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

        const fetchDatabases = async () => {
            try {
                let data = await getUsersDatabases();
                setDatabases(data.databases);
            } catch (error) {
                console.error("Error fetching databases:", error);
                setDatabases([]);
            }
        };

        fetchTables();
        fetchDatabases();

    }, [dbid, refreshKey]);



    


    return (
        <SidebarUI>
            <SidebarHeader className="">
                <DBSwitcher teams={
                    databases.map((db) => ({
                        id: db.id,
                        name: db.name,
                        logo: Database,
                        tables: db.tables,
                        size: db.size
                    }))
                }
                defaultTeamID={dbid || "default"}
                />
            </SidebarHeader>
            <SidebarContent className="mt-0">
                <SidebarGroup>

                </SidebarGroup>
                <SidebarGroup>
                    <div className="flex gap-1">
                        <Input placeholder="Search tables..." />
                        <Popover>
                                <PopoverTrigger asChild>
                                    {/* <SquareIconButton icon={<Plus />} label="Add Table"  className="h-9" /> */}
                                    <Button variant="outline" className=" w-fit h-9 aspect-square" >
                                        <Plus />
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent className="w-72" side="right">
                                    <form onSubmit={(e) => {
                                        e.preventDefault();
                                        createTable((e.currentTarget.elements.namedItem("tableName") as HTMLInputElement).value, dbid || "")
                                    }}>
                                        <span>New Table</span>
                                        <div className="flex flex-col gap-2 mt-2">
                                            <Input placeholder="Table Name" type="text" name="tableName" />
                                            <Button variant="outline" className="w-full" type="submit" >Create</Button>
                                        </div>
                                    </form>
                                </PopoverContent>
                            </Popover>
                        </div>
                    <ScrollArea>
                        {
                            tables && tables.length > 0 ? tables.map((table) => (
                                <ContextMenu key={table.id}>
                                    <ContextMenuTrigger>
                                        <Button variant="ghost" className={"w-full" + (selectedTable === table.id ? " bg-muted" : "")} onClick={() => { setSelectedTable(table.id); }}>
                                            <div className="flex flex-row gap-2 items-center justify-start w-full">
                                                <Table2 />
                                                <span>{table.name}</span>
                                            </div>
                                            <span className="text-xs text-muted-foreground font-normal">{table.rows}</span>
                                        </Button>

                                    </ContextMenuTrigger>
                                    <ContextMenuContent>
                                        <div className="flex items-center p-2"><Table2 size="16" /><span className="text-sm font-sans px-2">{table.name}</span></div>
                                        <hr className="mx-2 my-1"/>
                                        <ContextMenuItem><Plus />New</ContextMenuItem>
                                        <ContextMenuSub>
                                          <ContextMenuSubTrigger className="text-sm flex flex-row items-center gap-2 text-accent-foreground">
                                            <Edit className="text-muted-foreground" /> Rename
                                          </ContextMenuSubTrigger>
                                          <ContextMenuSubContent className="p-0 w-64">
                                            <form
                                              onSubmit={(e) => {
                                                e.preventDefault();
                                                // handle rename
                                                const formData = new FormData(e.currentTarget);
                                                const newName = formData.get("tableName") as string;
                                                if (newName.trim() !== "") {
                                                  tableAction(dbid || "", table.id, 'action.rename', { newname: newName, tableid: table.id });
                                                  setRefreshKey(Date.now());
                                                }
                                              }}
                                            >
                                              <div className="flex flex-row  ">
                                                <Input placeholder="Table Name" name="tableName" type="text" defaultValue={table.name} />
                                                <Button variant="outline" className="ml-2" type="submit" size={"icon"}>
                                                  <Check />
                                                </Button>
                                              </div>
                                            </form>
                                          </ContextMenuSubContent>
                                        </ContextMenuSub>
                                        <ContextMenuItem onClick={() => {tableAction(dbid || "", table.id, 'action.duplicate'); setRefreshKey(Date.now());}}><Copy />Duplicate</ContextMenuItem>
                                        <hr className="mx-2 my-1"/>
                                        <ContextMenuItem onClick={() => {tableAction(dbid || "", table.id, 'action.truncate'); setRefreshKey(Date.now());}}><ScissorsLineDashed />Truncate</ContextMenuItem>
                                        <ContextMenuItem className="text-destructive" onClick={() => {tableAction(dbid || "", table.id, 'action.delete'); setRefreshKey(Date.now());}}><Trash2 className="text-destructive"/>Drop</ContextMenuItem>
                                    </ContextMenuContent>
                                </ContextMenu>
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
                        <TooltipTrigger asChild><Button onClick={() => {window.location.href = "/home";}} variant="outline" className="w-fit h-auto aspect-square"><House /></Button></TooltipTrigger>
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