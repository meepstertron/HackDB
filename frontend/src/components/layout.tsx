import { title } from "process";
import ModularMenuBar from "./modularMenuBar";
import Sidebar, { EditorSidebar } from "./sidebar";
import { Pencil } from "lucide-react";
import { useMenuBar } from "./menuContext";
import React from "react";
import { SidebarProvider, SidebarTrigger } from "./ui/sidebar";

function RootLayout({ children }: React.PropsWithChildren) {
    const { menuItems, setMenuItems, title, setTitle } = useMenuBar();
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
    return (
        <SidebarProvider>
            <div className="h-screen w-screen flex text-gray-900">
                <EditorSidebar />
                <div className="flex flex-col flex-1">
                    
                    <header className="h-16 flex items-center px-6 border-b border-gray-300 bg-white">
                        <SidebarTrigger className="outline-1 outline-gray-300" />
                    </header>
                    
                    <main className="flex-1 overflow-auto">
                        {children}
                    </main>
                </div>
            </div>
        </SidebarProvider>
    )
}

export default RootLayout;
export { RootLayout, EditorLayout };