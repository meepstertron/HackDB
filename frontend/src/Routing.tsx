import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from "./App";
import RootLayout from "./components/layout";
import DBInfo from "./pages/databaseinfo";
import { DBPage } from "./pages/databases";
import { useContext } from "react";
import { AuthContext } from "./components/authContext";
import  "@/index.css"
import LoginPage from "./pages/login";




function Routing() {

    const { user, loading} = useContext(AuthContext);
    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen">
                <div className="loader_l17"></div>
                
                <p>Loading...</p>
            </div>
        );
    }


    return ( 
        <BrowserRouter>
{!user ? (
            <Routes>

                <Route path="*" element={<LoginPage />} />
            </Routes>
) : (<Routes>
  
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
          <Route path="*" element={
            
              <p>404 Not Found</p>
          } />
        </Routes>)}
      </BrowserRouter>
     );
}

export default Routing;