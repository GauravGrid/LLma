import { Box, Checkbox, IconButton,ListItemSecondaryAction,Modal, Typography } from '@mui/material';
import SideNav from './assets/components/sidenav';
import './repositories.css'
import React, { useState, useEffect } from 'react';
import {  CreateNewFolder, Folder } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

//button to share
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import { List, ListItem, ListItemText } from '@mui/material';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };


export default function Repositories() {
    
    const navigate = useNavigate()
    const jwtToken = sessionStorage.getItem("jwt")
    const [repositoryList, setRepositoryList] = useState([]);
    const urlParams = new URLSearchParams(window.location.search);
    const oauthIdentifier = urlParams.get('oauth_identifier');
    const [open, setOpen] = React.useState(false);
    const handleOpen = () => {
        setOpen(true)
        const selectedFiles = [...repositoryList];
        console.log("Selected files:", selectedFiles);
    };
    const handleClose = () => setOpen(false);
    const [selectedFiles, setSelectedFiles] = useState([]);

  const handleToggle = (file) => {
    const selectedIndex = selectedFiles.indexOf(file);
    const newSelected = [...selectedFiles];

    if (selectedIndex === -1) {
      newSelected.push(file);
    } else {
      newSelected.splice(selectedIndex, 1);
    }

    setSelectedFiles(newSelected);
  }
    //new added functionality to show checkboxed uploaded repo
// Function to retrieve selected files
// function retrieveSelectedFiles() {
//     const selectedFiles = [];
//     const checkboxes = document.querySelectorAll('input[name="selectedFiles"]:checked');

//     checkboxes.forEach(checkbox => {
//         selectedFiles.push(checkbox.value);
//     });

//     // Do something with the selected files (e.g., share them or perform an action)
//     console.log("Selected files:", selectedFiles);
// }

// // Add a click event listener to the "share" button
// const shareButton = document.getElementById("shareButton");
// shareButton.addEventListener("click", retrieveSelectedFiles);



    //changes end here
    useEffect(() => {
        if (oauthIdentifier) {
        fetch(`http://127.0.0.1:8000/associate-github-token?oauth_identifier=${oauthIdentifier}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Token ${jwtToken}`, 
            }
        })
            .then(response => response.json())
            .then(data => {
            console.log(data);
            })
            .catch(error => {
            console.error(error);
            });
        } else {
        }
        fetchProjects();
    }, []);
    const fetchProjects = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/upload', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token ${jwtToken}`, 
                },
            });

            if (response.ok) {
                const data = await response.json();
                setRepositoryList(data);
            } else {
                console.error('Failed to fetch projects');
            }
        } catch (error) {
            console.error('Error fetching projects:', error);
        }
    };

    const handleButtonClick = (projectId) => {
        return (event) => {
            event.preventDefault();
            navigate(`/dashboard?project=${projectId}`);
        }
    }
    const handleAddNew = ()=>{
        
            
            navigate('/upload');
        
        
    }
    return(
        
            
            <Box sx={{ display: "flex" }}>
          <SideNav />
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <div className='flex flex-col justify-center items-center' style={{ backgroundColor: '#FFF', height: '90vh', paddingTop: '64px' }}>
                <div className = 'repositoryHeading flex  items-start'>
                    <p>
                        Your Repositories
                    </p>
                </div>
               <div className='repositoryBox'>
                <div className='flex flex-row flex-wrap w-full'>
                {repositoryList.map((repository, index) => (
                                        <div key={index} className='flex flex-col max-w-min'>
                                            <IconButton className='folderButton' onClick={handleButtonClick(repository.project_id)} >
                                                <Folder className='folderIcon'/>
                                                <p className='folderName'>{repository.project_name}</p>
                                            </IconButton>
                                            
                                            
                                        </div>
                                ))}
                                <div className='flex flex-col'>
                                <IconButton className='folderButton' onClick={handleAddNew} >
                                                <CreateNewFolder className='folderIcon'/>
                                                <p className='folderName'>Add New</p>
                                </IconButton>
                                </div>
                                <div className="buttonToShare" id="shareButton">
                                <Stack spacing={2} direction="row" >
    
                                <Button sx={{backgroundColor:"#5F7A95"}} variant="contained" 
                                onClick={handleOpen}
                                >Share</Button>
                                <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              Select Files
            </Typography>
            <List>
      {repositoryList.map((file, index) => (
        <ListItem key={index} button>
        <Checkbox
          edge="start"
          checked={selectedFiles.indexOf(file) !== -1}
          onChange={() => handleToggle(file)}
        />
        <ListItemText primary={file.project_name} />
        <ListItemSecondaryAction>
          {/* You can add secondary actions (e.g., delete button) here */}
        </ListItemSecondaryAction>
      </ListItem>
      ))}
    </List>
    <Button onClick={()=>{
    }}>Continue</Button>
          </Box>
        </Modal>
                                </Stack>
                                </div>
                </div>
               
                </div>
             
                
            </div>
            
            </Box>
            </Box>
            
        
    )
}
