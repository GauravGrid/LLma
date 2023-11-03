import { Button, DialogActions, Divider, Typography,Select,MenuItem, Input } from "@mui/material";
import './gitpushmodal.css'
import { useState, useEffect } from 'react';



export default function NewBranchModal(props){
    const [name,setName] = useState('');
    const [branch,setBranch] = useState('');
    
    const handleBranchNameChange = (event) => {
        setName(event.target.value);
    };
    const handleBranchChange = (event) => {
        setBranch(event.target.value);
    }; 
    const createnewbranch = async (id) => {
        const jwtToken = sessionStorage.getItem("jwt");
        try {
          const response = await fetch(`http://127.0.0.1:8000/create-branch/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${jwtToken}`,
            },
            body: JSON.stringify({
                'repository_url': props.repinfo.repository_url,
                'branch_name': name,
                'start_branch':branch
            })
          })
          const data = await response.json();
          props.handleCloseBranchModal()
          props.getBranchList()
          console.log(data)
        } catch (error) {
          console.log(error)
        }
      }

    return(
        <div className="modal-box h-full">
            <div className="title-text mb-4 mt-4">
            <Typography className="title-text">Create New Branch</Typography>
            </div>
            <Divider className="divider"></Divider>
            
            <div className="input-box mt-4 mb-4">
                <Typography className="input-box-text">
                Enter New Branch Name
                </Typography>
                <Input value={name} onChange={handleBranchNameChange}></Input>
            </div>
            <Divider className="divider"></Divider>
            <div className="input-box mt-4 mb-4">
                <Typography className="input-box-text">
                Select Start Branch
                </Typography>
                <Select className='select' value={branch} onChange={handleBranchChange}>
                {
                        props.branchlist?.map((item, index) => (
                            <MenuItem value={item}>{item}</MenuItem>
                          ))
                    }
                </Select>
            </div>
            <Divider className="divider"></Divider>
            <DialogActions className="buttons">
                <Button className="cancel" onClick={props.handleCloseBranchModal} >
                    Cancel
                </Button>
                <Button variant="contained" className="push" onClick={createnewbranch}>
                    Create
                </Button>
            </DialogActions>
        </div>
    )
}