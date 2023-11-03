import React, { useState } from "react";
import {Resizable} from "re-resizable";
import { Box } from "@mui/material";
import { Split } from "@geoffcox/react-splitter";
const renderSplitter = (props) => {
    return <div className="w-5 h-full bg-primary"></div>
  };
const ResizableBoxes = () => {
  
  
  return (
        <Split initialPrimarySize="90%" minPrimarySize="30%" minSecondarySize='10%' renderSplitter={renderSplitter}>
            <div style={{height:'100vh'}}>
                hi
            </div>
            <div>
                hello
            </div>
           

        </Split>
  );
};

export default ResizableBoxes;
