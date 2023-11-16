import SideNav from "./assets/components/sidenav";
import { Box, TextField } from '@mui/material';
import './search.css';
import SearchIcon from '@mui/icons-material/Search';
import InputAdornment from '@mui/material/InputAdornment';
import React, { useMemo, useState, useEffect } from "react";
import {
    MaterialReactTable,
    useMaterialReactTable,
} from 'material-react-table';

const data = [
    {
        fileID: '3f25309c-8fa1-470f-811e-cdb082ab9017', //we'll use this as a unique row id
        fileName: 'File 1',
        lastModified: '22/11/2023',
        fileSize: '2 KB',
        
    }, //data definitions...
    {
        fileID: 'be731030-df83-419c-b3d6-9ef04e7f4a9f',
        fileName: 'File 2',
        lastModified: '18/11/2023',
        fileSize: '4 KB',
    },
    //end
];


export default function Search() {
    const columns = useMemo(
        //column definitions...
        () => [
            {
                accessorKey: 'fileName',
                header: 'File Name',
            },
            {
                accessorKey: 'lastModified',
                header: 'Last Modified',
            },
            {
                accessorKey: 'fileSize',
                header: 'File Size',
            }
        ],
        [], //end
    );

    //optionally, you can manage the row selection state yourself
    const [rowSelection, setRowSelection] = useState({});

    const table = useMaterialReactTable({
        columns,
        data,
        enableRowSelection: true,
        getRowId: (row) => row.fileID, //give each row a more useful id
        onRowSelectionChange: setRowSelection, //connect internal row selection state to your own
        state: { rowSelection }, //pass our managed row selection state to the table to use
        enableGlobalFilter: false,
        enableFullScreenToggle: false,
        getRowId: (originalRow) => originalRow.fileID,
    });

    //do something when the row selection changes...
    useEffect(() => {
        // console.log({ rowSelection }); //read your managed row selection state
        console.log(table.getState().rowSelection); //alternate way to get the row selection state
    }, [rowSelection]);

    return (
        <Box sx={{ display: "flex" }}>
            <SideNav />
            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <div className='flex flex-col justify-center items-center' style={{ paddingTop: '64px' }}>
                    <p>Identify Feature Groups</p>
                    <TextField InputProps={{
                        startAdornment: (
                            <InputAdornment position="start">
                                <SearchIcon />
                            </InputAdornment>
                        ),
                    }} className="searchBox" placeholder="Search all modules" variant="outlined" />
                    {/* <p>Recommended: Writing, Writing Prompts, Productivity</p> */}
                </div>
                <MaterialReactTable table={table} />
            </Box>
        </Box>
    )
}
