import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiDrawer from '@mui/material/Drawer';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import { Stack } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import InteractiveArea from './splitter'
import SideNav from './assets/components/sidenav';
import {   TextField } from '@mui/material';
import { LeftArrow } from 'styled-icons/boxicons-solid';
import { RightArrow } from 'styled-icons/boxicons-regular';
import FolderStructure from './assets/components/repositoryStructureView';
import CodeBlock from './assets/components/code';
import { useLocation } from 'react-router-dom';
import { useState } from 'react';
import { colorScheme } from './assets/components/colors';

const drawerWidth = 240;

export default function Dashboard(props) {
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const projectId = searchParams.get('project');
    const [project,setProject] = useState(projectId)
    return (
      <>
      <Box sx={{ display: "flex" }}>
          <SideNav folderId={project} onNotLoggedIn={props.onNotLoggedIn} opened={true} page={'dashboard'}/>
          <Box component="main" sx={{ flexGrow: 1}}>
          <div className='flex' style={{ backgroundColor: '#FFF', height: '100vh', paddingTop: '64px' }}>

            <InteractiveArea folderId={project}/>
        </div>
        </Box>
        </Box>
      </>
    
  );
}