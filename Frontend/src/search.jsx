import SideNav from "./assets/components/sidenav";
import { Alert, Box, Button, MenuItem, Modal, TextField, Typography } from "@mui/material";
import "./search.css";
import SearchIcon from "@mui/icons-material/Search";
import InputAdornment from "@mui/material/InputAdornment";
import React, { useMemo, useState, useEffect } from "react";
import {
  MaterialReactTable,
  useMaterialReactTable,
} from "material-react-table";
import Drawer from "@mui/material/Drawer";
import Divider from "@mui/material/Divider";
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import Stack from '@mui/material/Stack';
//modal

//modal-end
const data = [
  {
    fileID: "3f25309c-8fa1-470f-811e-cdb082ab9017", //we'll use this as a unique row id
    fileName: "File 1",
    lastModified: "22/11/2023",
    fileSize: "2 KB",
  }, //data definitions...
  {
    fileID: "be731030-df83-419c-b3d6-9ef04e7f4a9f",
    fileName: "File 2",
    lastModified: "18/11/2023",
    fileSize: "4 KB",
  },
  //end
];

export default function Search() {

  const [openAlert, setOpenAlert] = React.useState(false);

  const handleClick = () => {
    setOpenAlert(true);
  };

  const handleCloseA = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpenAlert(false);
  };
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [businessLogic, setBusinessLogic] = useState('');
  const [state, setState] = React.useState({
    top: false,
    left: false,
    bottom: false,
    right: false,
  });
  //drawer
  const [stateA, setStateA] = React.useState({
    top: false,
    left: false,
    bottom: false,
    right: false,
  });

  const toggleDrawerA = (anchor, open) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }

    setState({ ...state, [anchor]: open });
  };

  const list = (anchor) => (
    <Box
      className="drawer"
      sx={{ width: anchor === "top" || anchor === "bottom" ? "auto" : 250 }}
      role="presentation"
      onClick={toggleDrawer(anchor, false)}
      onKeyDown={toggleDrawer(anchor, false)}
    >
      <Divider />

      <div className="drawerDiv">
        <p className="heading">create sub-module</p>
        <p className="sub-heading">sub module name</p>
     
      <input className="customer-search" placeholder="customer search"></input>
      <button onClick={ () => setDrawerOpen(false)} className="close-button">close</button>
      <button  onClick={handleClick}
     
     className="create-button">create</button>
      <Snackbar open={openAlert} autoHideDuration={6000} onClose={handleCloseA}>
  <Alert onClose={handleCloseA} severity="success" sx={{ width: '100%' }}>
    successfully created
  </Alert>
</Snackbar> 
</div>  
    </Box>
   
  );

  //drawer-end

  const columns = useMemo(
    //column definitions...
    () => [
      {
        accessorKey: "fileName",
        header: "File Name",
      },
      {
        accessorKey: "lastModified",
        header: "Last Modified",
      },
      {
        accessorKey: "fileSize",
        header: "File Size",
      },
    ],
    [] //end
  );
  const [tableData, setTableData] = useState([]);
  const [rowCount, setRowCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  let success=false;

  //optionally, you can manage the row selection state yourself
  const [rowSelection, setRowSelection] = useState({});
  const [searchValue, setSearchValue] = useState("");
  //modal
  const [openModal, setOpenModal] = React.useState(false);
const handleOpen = (value) => {
    console.log(value)
    setOpenModal(true);
    handleBusinessLogicCall(value)                            
}
const handleClose = () => setOpenModal(false);

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      handleAPICall(searchValue);
    }
  };
  const handleChange = (event) => {
    setSearchValue(event.target.value);
  };
  const handleBusinessLogicCall = async (value) => {
    const jwtToken = sessionStorage.getItem("jwt");
    try {
      const response = await fetch(`http://127.0.0.1:8000/getlogic/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwtToken}`,
        },
        body: JSON.stringify({
          filename: value,
        }),
      });
      const data = await response.json();
      setBusinessLogic(data.data)

      
    } catch (error) {
      console.log(error);
    }
  };
  const handleAPICall = async (value) => {
    const jwtToken = sessionStorage.getItem("jwt");
    try {
      setIsLoading(() => true);
      const response = await fetch(`http://127.0.0.1:8000/search/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwtToken}`,
        },
        body: JSON.stringify({
          query: value,
        }),
      });
      const data = await response.json();
      console.log(data);

      const temp = data.data.map((file) => ({
        fileName: file,
        lastModified: "",
        fileSize: "10",
      }));
      console.log("temp: ", temp);
      setTableData(() => temp);
      setRowCount(() => temp.length);
      setIsLoading(() => false);

      console.log("tableData after set state: ", tableData);
    } catch (error) {
      console.log(error);
    }
  };
  const table = useMaterialReactTable({
    columns,
    data: tableData,
    enableRowSelection: true,
    getRowId: (row) => row.fileID, //give each row a more useful id
    onRowSelectionChange: setRowSelection, //connect internal row selection state to your own
    state: { rowSelection, isLoading },
    rowCount, //pass our managed row selection state to the table to use
    enableGlobalFilter: false,
    enableFullScreenToggle: false,
    getRowId: (originalRow) => originalRow.fileID,
    renderTopToolbarCustomActions: ({ table }) => (
      <Box sx={{ display: "flex", gap: "1rem", p: "4px" }}>
        <Button
          color="primary"
          onClick={() => {
            setDrawerOpen(true);
          }}
          variant="contained"
        >
          Create sub-module
        </Button>
      </Box>
    ),
    enableRowActions:true,
    renderRowActionMenuItems: ({ row }) => [
      <MenuItem key="open" onClick={() => handleOpen(row.original.fileName)}>
        open
      </MenuItem>,
     
    ],
  });

  const toggleDrawer = (anchor, open) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }

    setState({ ...state, [anchor]: open });
  };

  //do something when the row selection changes...
  useEffect(() => {
    // console.log({ rowSelection }); //read your managed row selection state
    console.log(table.getState().rowSelection); //alternate way to get the row selection state
  }, [rowSelection]);

  return (
    <>
      <>
        <div>
          <Button onClick={handleOpen}>Open modal</Button>
          
        </div>
        
    <Box sx={{ display: "flex" }}>
          <SideNav />
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <div
              className="flex flex-col justify-center items-center"
              style={{ paddingTop: "64px", paddingBottom: "2rem" }}
            >
              <p>Identify Feature Groups</p>
              <TextField
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
                className="searchBox"
                placeholder="Search all modules"
                variant="outlined"
                onKeyDown={handleKeyPress}
                onChange={handleChange}
                value={searchValue}
              />
              {/* <p>Recommended: Writing, Writing Prompts, Productivity</p> */}
            </div>
            {tableData.length !== 0 && <MaterialReactTable table={table} />}
            <div>
              <Drawer
                anchor={"right"}
                open={drawerOpen}
                onClose={() => setDrawerOpen(false)}
                sx={{
                //   paddingBottom: "10rem",
                //   height: "100vh",
                }}
                PaperProps={{
                  sx: {
                    // paddingBottom: "1rem",
                    boxSizing: "border-box",
                    // height: "100vh",
                  },
                }}
              >
                {list("right")}
              </Drawer>
            </div>
          </Box>
          <Modal
          className="modal-box"
            open={openModal}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
          >
            <div className="modal-content h-2/3 overflow-y-scroll p-3"> 

              <Typography id="modal-modal-title" variant="h6" component="h2">
                Business Logic
              </Typography>
              <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                {businessLogic.split(/\n/).map(line => <div key={line}>{line}</div>)}
              </Typography>

              
            </div>
          </Modal>
                  </Box>

      </>
      
    </>
    
  );
}
