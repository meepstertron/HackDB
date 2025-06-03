import { title } from "process";
import ModularMenuBar from "./modularMenuBar";
import Sidebar, { EditorSidebar, SquareIconButton } from "./sidebar";
import { motion, AnimatePresence } from "framer-motion"
import { Database, GitCommitVertical, Loader2, Plus, Redo2, Trash2, Undo2 } from "lucide-react"
import { Pencil } from "lucide-react";
import { useMenuBar } from "./menuContext";
import React, { useEffect, useState } from "react";
import { SidebarProvider, SidebarTrigger } from "./ui/sidebar";
import { r } from "node_modules/framer-motion/dist/types.d-CQt5spQA";
import { Button } from "./ui/button";
import { useEditorContext } from "@/editorContext";
import { Input } from "./ui/input";
import { Tooltip } from "@radix-ui/react-tooltip";
import { TooltipContent, TooltipTrigger } from "./ui/tooltip";
import { commitChanges } from "@/lib/api";
import { toast } from "sonner";
import { useParams } from "react-router-dom";
import { constructWhereClause } from "@/pages/editor";

function RootLayout({ children }: React.PropsWithChildren) {
    const { menuItems, setMenuItems, title, setTitle  } = useMenuBar();
    return (
        <div className="h-screen w-screen flex text-gray-900">
            <Sidebar />
            <div className="flex flex-col flex-1">
                
                <header className="h-16 flex items-center px-6 border-b bg-white">
                    {/* <ModularMenuBar menuItems={[
                        { name:"Database", onClick: () => console.log('Database clicked'), items:[
                            { name: "New", onClick: () => console.log('New clicked') },
                        ] },
                        { name: "Edit" },
                        { name: "View" },


                    ]} title="HackDB" /> */}

                    <ModularMenuBar title={title} menuItems={menuItems}/>
                </header>
                
                <main className="flex-1 p-6 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );
}

function EditorLayout({ children}: React.PropsWithChildren) {
  const { dbid } = useParams();
    // const [loading, setLoading] = useState(true);
    const { changes, limit, setLimit, offset, setOffset, selectedRows, timetaken, data, setChanges, selectedTable, setData, setSelectedRows } = useEditorContext();

    const handleCommit = () => {
        console.log("Commit changes");
        console.log("Changes: ", changes);
        if (changes.length === 0) {
            toast.error("No changes to commit");
            return;
        }
        commitChanges(changes, dbid || "")
            .then((response) => {
                if (response) {
                    console.log("Changes committed successfully:", response);
                    toast.success("Changes committed successfully... Please give it a moment to reflect in db");
                }
            })
            .catch((error) => {
                console.error("Error committing changes:", error);
                toast.error("Error committing changes");
            });
        setChanges([]);
    }

    return (
        <>
            {/* {loading && (
                <div className="flex items-center justify-center h-screen">
                    <LoadingScreen />
                </div>
            )} */}
            
            
            <SidebarProvider className={false ? "hidden" : ""}>
                <div className="h-screen w-screen flex text-gray-900">
                    <EditorSidebar />
                    <div className="flex flex-col flex-1">
                        
                        <header className="h-16 flex items-center justify-between px-6 border-b border-gray-300 bg-white">
                            <div className="flex items-center gap-4">
                              <SidebarTrigger className="outline-1 outline-gray-300" />
                              <div className="flex items-center gap-2">
                                <SquareIconButton icon={<Undo2 />} label="Undo" onClick={() => {}} className="h-9" />
                                <SquareIconButton icon={<Redo2 />} label="Redo" onClick={() => {}} className="h-9" />
                              </div>
                              <Button variant="outline"><Plus /> Add Row</Button>
                              {selectedRows.length > 0 && (
                              <Button variant="destructive" onClick={() => {
                                console.log("Delete selected rows:", selectedRows);

                                // Find the rows to delete by their unique IDs
                                const rowsToDelete = data.filter(row => selectedRows.includes(row.hiddenRowIDforFrontend));

                                // Add a delete change for each row
                                setChanges(prev => [
                                    ...prev,
                                    ...rowsToDelete.map(rowData => {
                                        let whereClause = constructWhereClause(rowData);
                                        delete whereClause.hiddenRowIDforFrontend;
                                        return {
                                            where: whereClause,
                                            table: selectedTable,
                                            type: "delete",
                                            timestamp: new Date().toISOString(),
                                        };
                                    }),
                                ]);

                                // Remove the deleted rows from data
                                setData(prev => prev.filter(row => !selectedRows.includes(row.hiddenRowIDforFrontend)));
                                setSelectedRows([]); // Clear selected rows after deletion
                            }}>
                                <Trash2 />
                                <span className="ml-2">Delete {selectedRows.length} Row{selectedRows.length === 1 ? "" : "s"}</span>
                              </Button>
                              )}
                            </div>
                            <div className="flex items-center gap-2 h-full">
                                <span className="mx-3 text-xs text-muted-foreground" title={timetaken + "ms"} >{data.length} Rows - {timetaken.toFixed(2)}ms</span>
                                <div className="flex items-center ">
                                    <Button variant="outline" className="rounded-none rounded-l w-4" onClick={() => {setOffset(offset - limit)}}>{"<"}</Button>
                                    <Tooltip>
                                        <TooltipTrigger asChild>
                                            <Input value={limit} onBlur={(e) => setLimit(Number(e.target.value))} onChange={(e) => setLimit(Number(e.target.value))} className="rounded-none w-12 text-center" />
                                        </TooltipTrigger>
                                        <TooltipContent>
                                            <p>Limit</p>
                                        </TooltipContent>
                                        
                                    </Tooltip>
                                    <Tooltip>
                                        <TooltipTrigger asChild>
                                            <Input value={offset} onBlur={(e) => setOffset(Number(e.target.value))} onChange={(e) => setOffset(Number(e.target.value))} className="rounded-none w-12 text-center" />
                                        </TooltipTrigger>
                                        <TooltipContent>
                                            <p>Offset</p>
                                        </TooltipContent>
                                    </Tooltip>
                                    <Button variant="outline" className="rounded-none rounded-r w-4" onClick={() => {setOffset(offset + limit)}}>{">"}</Button>
                                </div>
                                <Button variant="outline" className="justify-center items-center" onClick={handleCommit}>
                                    <GitCommitVertical />
                                    <span className="ml-2">Commit</span>
                                    <span className="ml-2 text-xs font-normal">{changes.length > 99 ? "99+" : changes.length}</span>
                                </Button>
                            </div>
                        </header>
                        
                        <main className="flex-1 overflow-auto">
                            {children}
                        </main>
                    </div>
                </div>
            </SidebarProvider>
        </>
    )
}


function LoadingScreen() {

    const randomInt = (min: number, max: number): number => {
        return Math.floor(Math.random() * (max - min)) + min;
    };

    const sillyTexts = [
    "applying database magic",
    "Scheming with Heidi",
    "Thinking about shipping with dinobox",
    "Herding selects",
    "Saging the servers",
    "Summoning the database spirits",
    "finding friends for foreign keys",
    ]
  const [currentTextIndex, setCurrentTextIndex] = useState(randomInt(0, sillyTexts.length))
  const [dots, setDots] = useState(".")


  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTextIndex((prevIndex) => (prevIndex + 1) % sillyTexts.length)
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const dotsInterval = setInterval(() => {
      setDots((prevDots) => (prevDots.length >= 3 ? "." : prevDots + "."))
    }, 500)

    return () => clearInterval(dotsInterval)
  }, [])

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4">
      <div className="flex flex-col items-center max-w-md text-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1, rotate: 360 }}
          transition={{
            type: "spring",
            stiffness: 260,
            damping: 20,
            duration: 1,
          }}
          className="relative mb-8"
        >
          <Database className="size-16 " />

        </motion.div>

        <h1 className="text-2xl font-bold mb-2 ">Setting Up Your Database Editor</h1>

        <div className="h-20 flex items-center justify-center mb-6">
          <AnimatePresence mode="wait">
            <motion.p
              key={currentTextIndex}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
              className="text-lg "
            >
              {sillyTexts[currentTextIndex]}
              <span className="inline-block w-8">{dots}</span>
            </motion.p>
          </AnimatePresence>
        </div>

      </div>
    </div>
  )
}

export default RootLayout;
export { RootLayout, EditorLayout };