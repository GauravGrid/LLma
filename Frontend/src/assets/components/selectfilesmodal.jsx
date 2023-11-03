import './gitpushmodal.css'
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { List, ListItem, ListItemText, Collapse, ListItemIcon, ListItemButton ,Typography,Checkbox} from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import { ArrowDropDown, Description, FolderSpecialTwoTone } from '@mui/icons-material';
import { colorScheme } from './colors';
import { Button, DialogActions} from "@mui/material";



export default function SelectFilesModal(props){


  const [folderData, setFolderData] = useState(null);
  const jwtToken = sessionStorage.getItem('jwt');
  const [selectedFiles, setSelectedFiles] = useState(props.selectedfilelist);
  const handleAdd = () => {
    const newSelectedfilelist = [...selectedFiles];
    props.setSelectedfilelist(newSelectedfilelist);
    console.log(newSelectedfilelist)
    props.handleCloseSelectFiles();
  };
  useEffect(() => {
    setSelectedFiles(props.selectedfilelist);
  }, [props.openSelectFilesModal,props.selectedfilelist]);
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
        setFolderData(responseData);

        const selectedFileIds = props.selectedfilelist.map(selectedFile => selectedFile.id);
        const initiallySelectedFiles = responseData.files.filter(file => selectedFileIds.includes(file.id));
        setSelectedFiles(initiallySelectedFiles);
      } catch (error) {
        console.log(error);
      }
    };

    fetchFolderData();
  }, [props.folderId, jwtToken, props.selectedfilelist]);
 

  const renderFolder = (folder, level = 0) => {
    const handleClick = () => {
      folder.open = !folder.open;
      setFolderData({ ...folderData });
    };
    const handleFileSelect = (file) => {
        console.log(file.id)
        const isSelected = selectedFiles.some((selectedFile) => selectedFile.id === file.id);
    
        if (isSelected) {
          setSelectedFiles(selectedFiles.filter((selectedFile) => selectedFile.id !== file.id));
        } else {
          setSelectedFiles([...selectedFiles, file]);
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
              <ListItemButton sx={{ height: '30px' }} key={file.id} style={fileIndentStyle}>
                <Checkbox
                  checked={selectedFiles.some((selectedFile) => selectedFile.id === file.id)}
                  onChange={() => handleFileSelect(file)}
                />
                <ListItemIcon sx={{ minWidth: '25px' }}>
                  <Description sx={{ width: '19px', height: '19px', color: '#FFF' }} />
                </ListItemIcon>
                <ListItemText
                  sx={{ fontSize: '14px' }}
                  primary={<Typography variant="body2" sx={{ fontSize: '13px', color: '#FFF' }}>{file.filename}</Typography>}
                />
              </ListItemButton>
            ))}
          </List>
        </Collapse>
      </div>
    );
  };

    
    
    return(
        <div className="modal-box h-full">
           <div className="overflow-y-scroll overflow-x-scroll h-full w-full" style={{backgroundColor:colorScheme.menu_secondary}}>
      
      <List className="flex flex-col justify-start" component="nav" aria-labelledby="folder-list">
        {folderData && renderFolder(folderData)}
      </List>
      
      
    </div>
    <DialogActions className="buttons relative bottom-0">
                <Button className="cancel" onClick={props.handleCloseBranchModal} >
                    Cancel
                </Button>
                <Button variant="contained" className="push" onClick={handleAdd}>
                    Add
                </Button>
            </DialogActions>
        </div>
    )
}




