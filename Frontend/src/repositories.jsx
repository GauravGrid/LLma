import { Box, IconButton } from '@mui/material';
import SideNav from './assets/components/sidenav';
import './repositories.css'
import React, { useState, useEffect } from 'react';
import { CreateNewFolder, Folder } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

export default function Repositories() {

    const navigate = useNavigate()
    const jwtToken = sessionStorage.getItem("jwt")
    const [repositoryList, setRepositoryList] = useState([]);
    const urlParams = new URLSearchParams(window.location.search);
    const oauthIdentifier = urlParams.get('oauth_identifier');


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
    const handleAddNew = () => {
        navigate('/upload');
    }

    return (
        <Box sx={{ display: "flex" }}>
            <SideNav />
            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <div className='flex flex-col justify-center items-center' style={{ backgroundColor: '#FFF', height: '90vh', paddingTop: '64px' }}>
                    <div className='repositoryHeading flex  items-start'>
                        <p>
                            Your Repositories
                        </p>
                    </div>
                    <div className='repositoryBox'>
                        <div className='flex flex-row flex-wrap w-full h-full overflow-y-scroll'>
                            {repositoryList.map((repository, index) => (
                                <div key={index} className='flex flex-col max-w-min'>
                                    <IconButton className='folderButton' onClick={handleButtonClick(repository.project_id)} >
                                        <Folder className='folderIcon' />
                                        <p className='folderName'>{repository.project_name}</p>
                                    </IconButton>
                                </div>
                            ))}
                            <div className='flex flex-col'>
                                <IconButton className='folderButton' onClick={handleAddNew} >
                                    <CreateNewFolder className='folderIcon' />
                                    <p className='folderName'>Add New</p>
                                </IconButton>
                            </div>
                        </div>
                    </div>
                </div>
            </Box>
        </Box>


    )
}