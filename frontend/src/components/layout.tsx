import Sidebar from "./sidebar";

function RootLayout({ children }: React.PropsWithChildren) {
    return (
        <div className="h-screen w-screen flex text-gray-900">
            <Sidebar />
            <div className="flex flex-col flex-1">
                
                <header className="h-16 flex items-center px-6 border-b bg-white">
                    <h1 className="text-xl font-semibold">Header</h1>
                </header>
                
                <main className="flex-1 p-6 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );
}

export default RootLayout;