import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import './index.css'
import Routing from './Routing'
import { AuthProvider } from './components/authContext'
import { MenuBarProvider } from './components/menuContext'




createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <MenuBarProvider>
        <Routing />
      </MenuBarProvider>
    </AuthProvider>
  </StrictMode>,
)
