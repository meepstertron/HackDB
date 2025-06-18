import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import './index.css'
import Routing from './Routing'
import { AuthProvider } from './components/authContext'
import { MenuBarProvider } from './components/menuContext'
import { EditorProvider } from './editorContext'
import { Toaster } from './components/ui/sonner'
import { ThemeProvider } from './components/theme-provider'




createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider defaultTheme='light' storageKey='vite-ui-theme'>
      <AuthProvider>
        <EditorProvider>
          <MenuBarProvider>
            <Routing />
          </MenuBarProvider>
        </EditorProvider>
      </AuthProvider>
      <Toaster />
    </ThemeProvider>
  </StrictMode>,
)
