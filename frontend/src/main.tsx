import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './index.css'
import App from './App.tsx'
import RootLayout from './components/layout.tsx'
import { DBPage } from './pages/databases.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>

        <Route path='/home' element={
            <RootLayout>
              <App />
            </RootLayout>
        } />
        <Route path='/databases' element={
          <RootLayout>
            <DBPage />
          </RootLayout>
        }/>
      </Routes>

    </BrowserRouter>
  </StrictMode>,
)
