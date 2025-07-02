import { BrowserRouter, Route, Routes } from "react-router-dom";
import App from "./App";
import RootLayout, { EditorLayout, FlowEditorLayout } from "./components/layout";
import DBInfo from "./pages/databaseinfo";
import { DBPage } from "./pages/databases";
import { useContext } from "react";
import { AuthContext } from "./components/authContext";
import  "@/index.css"
import LoginPage from "./pages/login";
import DatabaseCreationPage from "./pages/createdb";
import TableEditor from "./pages/editor";
import TokenPage from "./pages/tokens";
import FlowEditor from "./pages/FlowEditor";
import AddNodeOnEdgeDrop from "./pages/test";
import SettingsPage from "./pages/Settings";
import QuotaPage from "./pages/quota";




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
              <DatabaseCreationPage />
            </RootLayout>
          }/>
          <Route path='/databases/:id' element={
            <RootLayout>
              <DBInfo />
            </RootLayout>
          }/>
          <Route path="/editor/:dbid" element={
            <EditorLayout>
              <TableEditor />
            </EditorLayout>
          }/>
                    <Route path="/editor" element={
            <EditorLayout>
              <TableEditor />
            </EditorLayout>
          }/>

          <Route path="/tokens" element={
            <RootLayout>
              <TokenPage />
            </RootLayout>
          }/>
          <Route path="/flow" element={
            <FlowEditorLayout>
              <FlowEditor />
            </FlowEditorLayout>
          } />

          <Route path="/settings" element={
            <RootLayout>
              <SettingsPage />
            </RootLayout>
          } />
          <Route path="/quota" element={
            <RootLayout>
              <QuotaPage />
            </RootLayout>
          } />
          <Route path="*" element={

              <p>404 Not Found</p>
          } />
        </Routes>)}
      </BrowserRouter>
     );
}

export default Routing;