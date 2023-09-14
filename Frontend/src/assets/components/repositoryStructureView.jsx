import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { List, ListItem, ListItemText, Collapse, ListItemIcon, ListItemButton ,Typography} from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import { ArrowDropDown, Description, FolderSpecialTwoTone } from '@mui/icons-material';

import useAppStore from './states';
import { colorScheme } from './colors';

const FolderStructure = (props) => {
  const [folderData, setFolderData] = useState(null);
  const jwtToken = sessionStorage.getItem('jwt');

  useEffect(() => {
    const fetchFolderData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/upload/${props.folderId}`, {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${jwtToken}`,
          },
        });
        const responseData = response.data;
        
        
        setFolderData(response.data);
      } catch (error) {
        console.log(error);
        const responseData = error.response.data;
        if (responseData.detail === 'Invalid token') {
          console.log('not logged in')
          props.onNotLoggedIn();
          return;
        }
      }
    };

    fetchFolderData();
  }, [props.folderId, jwtToken,props.onNotLoggedIn]);
  const updateFileContent = useAppStore((state) => state.updateFileContent);
  const updateSelectedFileID = useAppStore((state) => state.updateSelectedFileID);
  const updateFileName = useAppStore((state) => state.updateFileName);
  const setIsGenButtonClicked = useAppStore((state)=>state.setIsGenButtonClicked)

  const renderFolder = (folder, level = 0) => {
    const handleClick = () => {
      folder.open = !folder.open;
      setFolderData({ ...folderData });
    };

    const handleFileClick = async(fileId) => {
        updateSelectedFileID(fileId)
        setIsGenButtonClicked(false)
        try {
          const response = await axios.get(`http://127.0.0.1:8000/file/${fileId}`, {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Token ${jwtToken}`,
            },
          });          
          updateFileName(response.data.filename)
          updateFileContent(response.data.file);
        } catch (error) {
          console.log(error);
          const responseData = error.response.data;
          if (responseData.detail === 'Invalid token') {
            console.log('not logged in')
            props.onNotLoggedIn();
            return;
          }
        
    };}
    const indentStyle = { paddingLeft: `${(level + 1) * 10}px` };
    const fileIndentStyle = { paddingLeft: `${(level + 2) * 10}px` };
  
    return (
      <div className='justify-start' key={folder.id}>
        <ListItemButton sx={{height:'30px'}} onClick={handleClick} style={indentStyle}>
        <ListItemIcon sx={{minWidth:'25px' ,}}>
            <FolderIcon sx={{width:'19px',height:'19px',color:'#FFF',dropShadow:'0px 2px 4px rgba(0, 0, 0, 0.1)'}}/>
          </ListItemIcon>
          <ListItemText  sx={{ fontSize: '14px',color:'#FFF' }} primary={<Typography variant="body2" sx={{ fontSize: '14px' }}>{folder.foldername}</Typography>} />
        </ListItemButton>
        <Collapse in={folder.open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {folder.subfolders.map((subfolder) => (
              <div key={subfolder.id}>
                {renderFolder(subfolder, level + 1)}
              </div>
            ))}
            {folder.files.map((file) => (
              <ListItemButton sx={{height:'30px'}} key={file.id} onClick={() => handleFileClick(file.id)} style={fileIndentStyle}>
                <ListItemIcon sx={{minWidth:'25px'}}>
                    <Description sx={{ width:'19px',height:'19px',color:'#FFF'}}/>
                </ListItemIcon>
                <ListItemText  sx={{ fontSize: '14px' }} primary={<Typography variant="body2" sx={{ fontSize: '13px',color:'#FFF' }}>{file.filename}</Typography>} />
              </ListItemButton>
            ))}
          </List>
        </Collapse>
      </div>
    );
  };
  
  

  return (
    <div className="flex flex-col h-full w-full" style={{backgroundColor:colorScheme.menu_secondary}}>
      <div className='flex justify-between p-2 w-full' style={{border:'1px solid #2B3140' , borderWidth:'2px 0'}}>
        <Typography sx={{color:'#FFF'}}>
          Source
        </Typography>
        {/* <ArrowDropDown sx={{color:'#FFF'}}/> */}
      </div>
      <div className="overflow-y-scroll overflow-x-scroll h-full w-full" style={{backgroundColor:colorScheme.menu_secondary}}>
      
      <List className="flex flex-col justify-start" component="nav" aria-labelledby="folder-list">
        {folderData && renderFolder(folderData)}
      </List>
    </div>
    </div>
    
  );
};

export default FolderStructure;
