import React, { createContext, useState, useContext, ReactNode } from 'react';


export interface MenuItem {
    name: string;
    icon?: string;
    onClick?: () => void;
    items?: MenuItem[];
}


interface MenuBarContextType {
    menuItems: MenuItem[];
    setMenuItems: (items: MenuItem[]) => void;
    title: string;
    setTitle: (title: string) => void;
}


const MenuBarContext = createContext<MenuBarContextType | undefined>(undefined);


export const MenuBarProvider = ({ children }: { children: ReactNode }) => {
    const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
    const [title, setTitle] = useState<string>("HackDB");

    return (
        <MenuBarContext.Provider value={{ menuItems, setMenuItems, title, setTitle }}>
            {children}
        </MenuBarContext.Provider>
    );
};

export const useMenuBar = () => {
    const context = useContext(MenuBarContext);
    if (context === undefined) {
        throw new Error('you cant use this without putting it in the envioronment');
    }
    return context;
};