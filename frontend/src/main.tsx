import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import './index.css'
import Routing from './Routing'
import { AuthProvider } from './components/authContext'
import { MenuBarProvider } from './components/menuContext'
import { EditorProvider } from './editorContext'




createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <EditorProvider>
        <MenuBarProvider>
          <Routing />
        </MenuBarProvider>
      </EditorProvider>
    </AuthProvider>
  </StrictMode>,
)
