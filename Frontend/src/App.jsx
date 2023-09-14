import './App.css'
import { Route, Routes, Navigate } from 'react-router-dom'
import Dashboard from './dashboard'
import React, { useState } from 'react';
import Login from './login';
import UploadScreen from './uploadScreen'
import { createTheme, Modal, ThemeProvider, Typography } from '@mui/material';
import FolderStructure from './assets/components/repositoryStructureView'
import MermaidDiagram from './assets/components/mermaid'
import Repositories from './repositories'
import { useNavigate } from 'react-router-dom';
import SignUp from './signup';
import ResizableBoxes from './assets/components/test';
import ResetOnPageReload from './assets/components/reset';
const theme = createTheme({
  typography: {
    fontFamily: [
      'Nunito',
      'sans-serif',
    ].join(','),
  },});
function App() {
  const navigate = useNavigate()

  const [showNotLoggedInPopup, setShowNotLoggedInPopup] = useState(false);

  const handleNotLoggedIn = () => {
    setShowNotLoggedInPopup(true);
  };

  const handleClosePopup = () => {
    setShowNotLoggedInPopup(false);
    navigate("/login");
  };
  
  return (
    <ThemeProvider theme={theme}>
        <Routes>
          <Route path='/dashboard' element={<Dashboard onNotLoggedIn={handleNotLoggedIn} />} />
          <Route path='/repositories' element={<Repositories onNotLoggedIn={handleNotLoggedIn}/>} />
          <Route path='/upload' element={<UploadScreen onNotLoggedIn={handleNotLoggedIn}/>} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />

          <Route path="/mermaid" element={<MermaidDiagram/>}/>
          <Route path='/folder' element={<FolderStructure folderId={2}/>}/>
          <Route path='/test' element={<ResizableBoxes/>}/>
          <Route path='*' element={<Navigate to='/login' />} />
        </Routes>
     
      {window.location.pathname !== '/login' &&  (
    
        <Modal open={showNotLoggedInPopup} onClose={handleClosePopup} style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
        <div className='h-40 bg-background w-40'>
        <Typography variant="h5">Not logged in</Typography>
            <Typography variant="body1">Please log in to access the folder data.</Typography>
            
          
        </div>
           
        </Modal>
        
        
      )}
      <ResetOnPageReload/>
      </ThemeProvider>
    
  )
}

export default App
