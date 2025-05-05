import { Database, Hash, PercentDiamondIcon, Settings2, Workflow } from "lucide-react";
// use react router dom to navigate between pages
import { useNavigate } from "react-router-dom";

function Sidebar() {
    const navigate = useNavigate();
    const elements = [
        { name: "Databases", icon: <Database />, location: "/databases", active: true },
        { name: "Workflows", icon: <Workflow />, location: "/workflows", active: false },
        { name: "Quota", icon: <PercentDiamondIcon />, location: "/quota", active: false },
        { name: "Tokens", icon: <Hash />, location: "/tokens", active: false },
        { name: "Settings", icon: <Settings2 />, location: "/settings", active: true },
    ];

    return ( 
        <aside className="w-16 h-full bg-white border-r flex flex-col items-center p-4">
            
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

export default Sidebar;