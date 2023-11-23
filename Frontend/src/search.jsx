import SideNav from "./assets/components/sidenav";
import { Box, Button, TextField } from "@mui/material";
import "./search.css";
import SearchIcon from "@mui/icons-material/Search";
import InputAdornment from "@mui/material/InputAdornment";
import React, { useMemo, useState, useEffect } from "react";
import {
  MaterialReactTable,
  useMaterialReactTable,
} from "material-react-table";
//drawer

import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';

//drawer-end

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

    const [drawerOpen, setDrawerOpen] = useState(false)




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
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }

    setState({ ...state, [anchor]: open });
  };

  const list = (anchor) => (
    <Box
      sx={{ width: anchor === 'top' || anchor === 'bottom' ? 'auto' : 250 }}
      role="presentation"
      onClick={toggleDrawer(anchor, false)}
      onKeyDown={toggleDrawer(anchor, false)}
    >
      {
        <h4>create sub module</h4>
      }
      <Divider />
      {/* <List>
        {['All mail', 'Trash', 'Spam'].map((text, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List> */}
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

  //optionally, you can manage the row selection state yourself
  const [rowSelection, setRowSelection] = useState({});
  const [searchValue, setSearchValue] = useState("");
  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      handleAPICall(searchValue);
    }
  };
  const handleChange = (event) => {
    setSearchValue(event.target.value);
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
            // alert("Create New Account");
            setState({ ...state, right: true });
         
            
          }}
          variant="contained"
        >
          Create sub-module
        </Button>
      </Box>
    ),
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
      {['right'].map((anchor) => (
        <React.Fragment key={anchor}>
          {/* <Button onClick={toggleDrawerA(anchor, true)}>{anchor}</Button> */}
          <Drawer 
            anchor={anchor}
            open={state[anchor]}
            onClose={toggleDrawerA(anchor, false)}
            
          >
            {list(anchor)}
          </Drawer>
        </React.Fragment>
      ))}
    </div>




      </Box>
    </Box>
  );
}
