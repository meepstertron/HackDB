import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from "./App";
import RootLayout from "./components/layout";
import DBInfo from "./pages/databaseinfo";
import { DBPage } from "./pages/databases";

function Routing() {
    return ( 
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
          <Route path='/databases/create' element={
            <RootLayout>
              <p>Create your awesome sauce db</p>
            </RootLayout>
          }/>
          <Route path='/databases/:id' element={
            <RootLayout>
              <DBInfo />
            </RootLayout>
          }/>
        </Routes>
      </BrowserRouter>
     );
}

export default Routing;