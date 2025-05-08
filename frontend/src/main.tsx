import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import './index.css'
import Routing from './Routing'
import { AuthProvider } from './components/authContext'




createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <Routing />
    </AuthProvider>
  </StrictMode>,
)
