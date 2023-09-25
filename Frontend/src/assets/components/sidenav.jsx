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
import AccountCircle from '@mui/icons-material/AccountCircle';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { deleteJwtToken } from '../../login';
import { useNavigate } from 'react-router-dom';
import {colorScheme} from './colors'
import UploadIcon from '@mui/icons-material/Upload';
import SourceIcon from '@mui/icons-material/Source';
import FolderStructure from './repositoryStructureView';
import CodeIcon from '@mui/icons-material/Code';
import  useAppStore  from './states';
import { ArrowDropDown, ImportContacts } from '@mui/icons-material';
import axios from "axios";





import FolderCopyIcon from '@mui/icons-material/FolderCopy';

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';




// githubicon

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';
import './sidenav.css'

const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    zIndex: theme.zIndex.drawer - 1,
    marginLeft: drawerWidth,
    width: '100%',
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }),
);

export default function SideNav(props) {
  const theme = useTheme();
  const updateFileContent = useAppStore((state) => state.updateFileContent);
  const updateFileName = useAppStore((state)=> state.updateFileName)


  // repourl

  const [cloneRepoUrl, setCloneRepoUrl] = React.useState('')


  // const [open, setOpen] = React.useState(false);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const updateOpen = useAppStore((state) => state.updateOpen);
  const open = (props.opened)? true :  useAppStore((state) => state.dopen);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  
  const navigate = useNavigate()
  const handleLogout = () =>{
    deleteJwtToken();
    navigate('/login')
  }
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleUploadRouting = (urls) =>{
    updateFileContent(null)
    updateFileName(null)
    navigate('/upload')
  }
  const handleDashBoardRouting = (urls) =>{
    navigate('/dashboard')
  }
  const handleRepositoryRouting = (urls) =>{
    navigate('/repositories')
  }
  const handleDrawerOpen = () => {
    updateOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };




  // event handling of gitclone

  // const [openSourcecontrol, setOpenSourcecontrol ]= React.useState(false);

  // const handleClonecontrolOpen = () => {
  //   setOpenSourcecontrol(true);
  // };

  // const handleClonecontrolClose = () => {
  //   setOpenSourcecontrol(false);
  // };

  // const handleCloneRepo = async(e) => {
  //     e.preventDefault();
  //     console.log(cloneRepoUrl)
  
  //     try {
  //       const response = await axios.post(
  //         "http://127.0.0.1:8000/login/",

  //         {  }
  //       );
  //       const  jwtToken  = response.data.token;
  //       sessionStorage.clear();
  //       setJwtToken(jwtToken);
  
  //       navigate("/repositories");
  //     } catch (error) {
  //       console.log(error);
  //       }
  //     }
    
  

      // github button
      
      const handleGitHubLogin = async () => {
        try {
          // Redirect the user to GitHub for authentication
          window.location.href = `https://github.com/login/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_CALLBACK_URL&scope=user`;
        } catch (error) {
          console.error('GitHub login error:', error);
        }
      };
  


  return (
    <Box sx={{  backgroundColor:colorScheme.menu_primary ,  }}>
      <CssBaseline />
      <AppBar position="fixed" open={open}>
        <Toolbar sx={{width:'100%' , backgroundColor : colorScheme.primary}}>
          <Typography variant="h5" component="div" sx={{ 
            flexGrow: 1,
             }}>
              CodeBridge
          </Typography>




          <button onClick={handleGitHubLogin} className="github-login-button">
              <FontAwesomeIcon icon={faGithub} /> Login to GitHub
          </button>
           
            {/* <div>
              <IconButton
              className='iconButton'
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
              >
                <AccountCircle />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem onClick={handleClose}>Profile</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </div> */}
          
        </Toolbar>
      </AppBar>
      <Drawer variant="permanent" open={(props.opened)?true:open}
      onMouseEnter={()=>{updateOpen(true)}}
      onMouseLeave={()=>(props.opened)?updateOpen(true):updateOpen(false)}
      PaperProps={{
        sx: {
          backgroundColor:'#535F7E',
          width: 240,
          zIndex:1000,
        }
      }}>
        <DrawerHeader>
          <IconButton>
            {theme.direction === "rtl" ? (
              <ChevronRightIcon />
            ) : (
              <ChevronLeftIcon />
            )}
          </IconButton>
            </DrawerHeader>
        <List sx={{backgroundColor : colorScheme.menu_secondary , height:'100vh' }}>



            <ListItem key={'Upload'} disablePadding  sx={{ display: 'block' }}>
              <ListItemButton
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                  color:'#FFFFFF'
                }}
                onClick={handleUploadRouting}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                    color:'#FFFFFF'
                  }}
                >
                  <UploadIcon /> 
                </ListItemIcon>
                <ListItemText primary={'Upload'} sx={{ opacity: open ? 1 : 0 ,color:'#FFFFFF'}} />
              </ListItemButton>
            </ListItem>


            <ListItem key={'Your Repositories'} disablePadding sx={{ display: 'block' }} >
            <ListItemButton
              sx={{
                minHeight: 48,
                justifyContent: open ? 'initial' : 'center',
                px: 2.5,
                color:'#FFFFFF'
              }}
              onClick={handleRepositoryRouting}
    
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: open ? 3 : 'auto',
                  justifyContent: 'center',
                  color:'#FFFFFF'
                }}
              >
                <SourceIcon/> 
              </ListItemIcon>
              <ListItemText primary={'Your Repositories'} sx={{ opacity: open ? 1 : 0 ,color:'#FFFFFF'}} />
            </ListItemButton>
          </ListItem>


          <ListItem key={'Dashboard'}  disablePadding sx={{ display: 'block' }}>
          <ListItemButton
            sx={{
              minHeight: 48,
              justifyContent: open ? 'initial' : 'center',
              px: 2.5,
              color:'#FFFFFF'
            }}
            onClick={handleDashBoardRouting}
          >
            <ListItemIcon
              sx={{
                minWidth: 0,
                mr: open ? 3 : 'auto',
                justifyContent: 'center',
                color:'#FFFFFF'
              }}
            >
               <CodeIcon/>
            </ListItemIcon>
            <ListItemText primary={'Code Converter'} sx={{ opacity: open ? 1 : 0 ,color:'#FFFFFF'}} />
          </ListItemButton>
        </ListItem>

        {/* FolderCopyIcon  */}


        {/* <ListItem key={'sourceControl'}  disablePadding sx={{ display: 'block' }}>
          <ListItemButton
            sx={{
              minHeight: 48,
              justifyContent: open ? 'initial' : 'center',
              px: 2.5,
              color:'#FFFFFF'
            }}
            onClick={handleClonecontrolOpen}
          >
            <ListItemIcon
              sx={{
                minWidth: 0,
                mr: open ? 3 : 'auto',
                justifyContent: 'center',
                color:'#FFFFFF'
              }}
            >
               <FolderCopyIcon/>
            </ListItemIcon>
            <ListItemText primary={'Source Control'} sx={{ opacity: open ? 1 : 0 ,color:'#FFFFFF'}} />
          </ListItemButton>
          <Dialog open={openSourcecontrol} onClose={handleClonecontrolClose}>
                <DialogTitle>Clone Repositories</DialogTitle>
                <DialogContent>
                  <DialogContentText>
                    To Clone github repository, please enter repo address here. 
                  </DialogContentText>
                  <TextField
                    autoFocus
                    margin="dense"
                    id="name"
                    label="Clone Repository"
                    type="address"
                    fullWidth
                    variant="standard"
                    onChange={(e) => setCloneRepoUrl(e.target.value)}
                  />
                </DialogContent>
                <DialogActions>
                  <Button onClick={handleClonecontrolClose}>Cancel</Button>
                  <Button onClick={handleCloneRepo}>Clone</Button>
                </DialogActions>
              </Dialog>
        </ListItem> */}


        </List>



        {props.folderId?
          <FolderStructure folderId={props.folderId} onNotLoggedIn={props.onNotLoggedIn}/>:
          (props.page==='dashboard')?
          <div>
             <div className=' p-2 w-full' style={{border:'1px solid #FFF' , borderWidth:'1px 0 1px 0',position:'absolute'}}>
        <Typography sx={{color:'#FFF' }}>
          Source
        </Typography>
        {/* <ArrowDropDown sx={{color:'#FFF'}}/> */}
      </div>
          <div className="overflow-y-scroll overflow-x-scroll bg-menu_primary h-full" style={{backgroundColor : colorScheme.menu_secondary}}>
            
      <List className="flex flex-col justify-start" component="nav" aria-labelledby="folder-list">
      <ListItem key={'Upload'} disablePadding  sx={{ display: 'block' }}>

          <ListItemButton sx={{
                minHeight: 48,
                marginTop:'34px',
                justifyContent: open ? 'initial' : 'center',
                px: 2.5,
                color:'#FFFFFF'
              }}
            onClick={handleRepositoryRouting}>



            <div style={{marginBottom:'22rem',marginLeft:'2rem'}}>
                <ListItemIcon sx={{
                    minWidth: 0,
                    mr: open ? 1 : 'auto',
                    justifyContent: 'centre',
                    color:'#FFFFFF'
                  }}>
              <ImportContacts/>
              <div style={{marginLeft:'1rem',marginBottom:'1rem'}}>
                  <ListItemText primary={'Open New'} />
              </div>
              </ListItemIcon>

            
            

            </div>
          </ListItemButton>
          </ListItem>
      </List>
    </div>
          </div>
         
          
          :
          <></>
        }



        <div style={{ display:'flex',marginLeft:'2px'}}>
              <IconButton
              className='iconButton'
                size="extra large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
              >
                <AccountCircle style = {{ fontSize:'25px'}}/>
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                // anchorOrigin={{
                //   vertical: 'bottom',
                //   horizontal: 'left',
                // }}
                keepMounted
                // transformOrigin={{
                //   vertical: 'top',
                //   horizontal: 'left',
                // }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem onClick={handleClose}>Profile</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </div>

            
      </Drawer>
      {/* <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <DrawerHeader />
        
      </Box> */}
     
     
    </Box>
  );
}