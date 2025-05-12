
import React from 'react';
import { Menubar, MenubarTrigger, MenubarMenu, MenubarContent, MenubarItem } from "./ui/menubar";
function ModularMenuBar(
    props: {
        menuItems?: Array<{ name: string; icon?: React.ReactNode; onClick?: () => void, items?: Array<{ name: string; icon?: string; onClick?: () => void }> }>;
        title?: string;
        onClick?: () => void;
    }


) {

    let shouldShowMenuOptions = false;
    if (props.menuItems && props.menuItems.length > 0) {
        shouldShowMenuOptions = true;

    }

    return ( 
        <>
        {props.title && <h1 className="text-xl font-semibold mr-4">{props.title}</h1>}
        {shouldShowMenuOptions && (
            <Menubar>
                
                    {props.menuItems?.map((item, index) => (
                        <MenubarMenu key={index}>
                            <MenubarTrigger>
                                {item.icon && <span className="mr-2">{item.icon}</span>}
                                {item.name}
                            </MenubarTrigger>
                            <MenubarContent>
                                {item.items && item.items.map((subItem, subIndex) => (
                                    <MenubarItem onClick={subItem.onClick} key={subIndex}>
                                        {subItem.name}
                                    </MenubarItem>
                                )
)}
                            </MenubarContent>
                        </MenubarMenu>
                    ))}               
            </Menubar>
        )}
        
        </>
     );
}

export default ModularMenuBar;