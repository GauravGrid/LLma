import { Button, DialogActions, Divider, Typography,Select,MenuItem, Input } from "@mui/material";
import './gitpushmodal.css'
import { useState, useEffect } from 'react';



export default function NewRepModal(props){
    const [desc,setDesc] = useState('');
    const [name,setName] = useState('');
    
    const handleRepNameChange = (event) => {
        setName(event.target.value);
    };
    const handleDescChange = (event) => {
        setDesc(event.target.value);
    };
    const createnewrep = async (id) => {
        const jwtToken = sessionStorage.getItem("jwt");
        try {
          const response = await fetch(`http://127.0.0.1:8000/create-git-repo/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${jwtToken}`,
            },
            body: JSON.stringify({
                'repository_name': name,
                'description': desc
            })
          })
          const data = await response.json();
          props.handleCloseRepModal()
          console.log(data)
        } catch (error) {
          console.log(error)
        }
      }
    return(
        <div className="modal-box h-full">
            <div className="title-text mb-4 mt-4">
            <Typography className="title-text">Create New Repository</Typography>
            </div>
            <Divider className="divider"></Divider>
            
            <div className="input-box mt-4 mb-4">
                <Typography className="input-box-text">
                Enter Repository Name
                </Typography>
                <Input value={name} onChange={handleRepNameChange}></Input>
            </div>
            <Divider className="divider"></Divider>
            <div className="input-box mt-4 mb-4">
                <Typography className="input-box-text">
                Enter Repository Description
                </Typography>
                <Input value={desc} onChange={handleDescChange}></Input>
            </div>
            <Divider className="divider"></Divider>
            <DialogActions className="buttons">
                <Button className="cancel" onClick={props.handleCloseRepModal}>
                    Cancel
                </Button>
                <Button variant="contained" className="push" onClick={createnewrep}>
                    Create
                </Button>
            </DialogActions>
        </div>
    )
}