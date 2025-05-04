import Sidebar from "./sidebar";

function RootLayout({ children }: React.PropsWithChildren) {
    return (
        <div className="h-screen w-screen flex bg-gray-100 text-gray-900">
            <Sidebar />
            <div className="flex flex-col flex-1">
                {/* Header */}
                <header className="h-16 flex items-center px-6 border-b bg-white">
                    <h1 className="text-xl font-semibold">Header</h1>
                </header>
                {/* Main Content */}
                <main className="flex-1 p-6 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );
}

export default RootLayout;