import { ThemeProvider } from "@mui/material/styles";
import theme, { colorScheme } from "./assets/components/colors";
import SideNav from "./assets/components/sidenav";
import {
    Box,
    Button,
    IconButton,
    TextField,
    Typography,
    createTheme,
} from "@mui/material";
import { styled } from "@mui/system";
import React, { useState, useRef, useEffect } from "react";
import {
    Close,
    Cloud,
    CloudUpload,
    FileUpload,
    Upload,
} from "@mui/icons-material";
import "./uploadScreen.css";
import { Cross, File } from "styled-icons/boxicons-regular";
import {
    FileArrowUp,
    FileArrowUpFill,
    FileEarmarkArrowUpFill,
} from "styled-icons/bootstrap";
import { FilePen } from "styled-icons/fa-solid";
import { useNavigate } from "react-router-dom";




// clone from git hub
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';



import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';




const FileDropBox = styled(Box)({
    width: "50%",
    border: "0.5px dashed #000",
    backgroundColor: "#2B2D32",
    boxShadow: "0px 4px 4px 0px rgba(0, 0, 0, 0.25)",
    padding: "18px",
    paddingLeft: "28px",
    paddingRight: "28px",
    overflow: "auto",
    whiteSpace: "pre-wrap",
    borderRadius: "30px",
});
const StyledTextField = styled(TextField)({
    width: "100%",
    "& .css-10botns-MuiInputBase-input-MuiFilledInput-input": {
        backgroundColor: "#4A4946",
    },

    "& .css-11g5tkx-MuiInputBase-root-MuiFilledInput-root": {
        "&:after": {
            borderBottomColor: "#FFF",
        },
        backgroundColor: "#4A4946",
    },
    "& .MuiInputBase-root.Mui-focused": {
        backgroundColor: "#4A4946",
        borderBottomColor: "#FFF",
    },

    "& .MuiInputBase-root": {
        color: "#FFF",
        "&:before": {
            borderBottomColor: "#FFF !important",
        },
        "&:hover:before": {
            borderBottomColor: "#FFF !important",
        },
        "&.Mui-focused": {
            color: "#FFF",
            borderBottomColor: "#FFF !important",
            "&:before": {
                borderBottomColor: "#FFF !important",
            },
        },
    },

    "& .MuiInputLabel-root": {
        color: "#FFF !important",
        "&.Mui-focused": {
            color: "#FFF !important",
        },
    },
});

export default function UploadScreen(props) {
    const [isProject, setIsProject] = useState(false);
    const [isDropped, setIsDropped] = useState(false);
    const [isRequired, setIsRequired] = useState(false);
    useEffect(() => {
        if (isProject ^ isDropped) {
            setIsRequired(true);
        } else {
            setIsRequired(false);
        }
    }, [isProject, isDropped]);

    const [fileContent, setFileContent] = useState("");
    const [projectName, setProjectName] = useState("");
    const [droppedFiles, setDroppedFiles] = useState([]);

    const [projectHelper, setProjectHelper] = useState("");
    const fileInputRef = useRef(null);
    const navigate = useNavigate();
    const handleDrop = (event) => {
        event.preventDefault();
        const files = Array.from(event.dataTransfer.files);
        handleFiles(files);
    };

    const handleDragOver = (event) => {
        event.preventDefault();
    };

    const handleBrowse = () => {
        fileInputRef.current.click();
    };

    const handleFiles = (files) => {
        setDroppedFiles((prevFiles) => [...prevFiles, ...files]);
        if (droppedFiles.length > 0) {
            setIsDropped(true);
        } else {
            setIsDropped(false);
        }
    };

    const handleInputChange = (event) => {
        const files = Array.from(event.target.files);
        document.getElementById("file-error").style.display = "none";
        if (files.length > 0) {
            setDroppedFiles((prevFiles) => [...prevFiles, ...files]);
            setIsDropped(true);
        } else {
            setIsDropped(false);
        }
    };

    const handleRemoveFile = (file) => {
        setDroppedFiles((prevFiles) => prevFiles.filter((f) => f !== file));
    };
    const handleRequired = () => {
        console.log("file uploaded");
        if (droppedFiles.length === 0) {
            if (projectName === "") {
                setProjectHelper("Required");
                document.getElementById("file-error").style.display = "block";
            }
        } else if (projectName === "") {
            setProjectHelper("Required");
        } else {
            if (droppedFiles.length > 0) {
                setProjectHelper("");
                handleUpload();
            } else {
                document.getElementById("file-error").style.display = "block";
            }
        }
    };
    const handleUpload = () => {
        const jwtToken = sessionStorage.getItem("jwt");
        const formData = new FormData();
        formData.append("project_name", projectName);
        const headers = new Headers();
        headers.append("Authorization", "Bearer " + jwtToken);

        if (
            droppedFiles.length === 1 &&
            droppedFiles[0].type === "application/zip"
        ) {
            // Handle zip file upload
            const zipFile = droppedFiles[0];
            formData.append("zip_file", zipFile);

            fetch("http://127.0.0.1:8000/upload", {
                method: "POST",
                headers: headers,
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    const responseData = data;
                    if (responseData.detail === "Invalid token") {
                        props.onNotLoggedIn();
                        return;
                    }
                    navigate("/repositories");
                })
                .catch((error) => {
                    // Handle error
                    console.error(error);
                });
        } else {
            // Handle individual file uploads
            droppedFiles.forEach((file) => {
                formData.append("files", file);
            });

            fetch("http://127.0.0.1:8000/upload", {
                method: "POST",
                headers: headers,
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    navigate("/repositories");
                })
                .catch((error) => {
                    // Handle error
                    console.error(error);
                });
        }
    };

     // event handling of gitclone

  const [openSourcecontrol, setOpenSourcecontrol ]= React.useState(false);

  const handleClonecontrolOpen = () => {
    setOpenSourcecontrol(true);
  };

  const handleClonecontrolClose = () => {
    setOpenSourcecontrol(false);
  };



  const handleCloneRepo = async(e) => {
      e.preventDefault();
      console.log(cloneRepoUrl)
  
    //   try {
    //     const response = await axios.post(
    //       "http://127.0.0.1:8000/clone/",

    //       {  data }
    //     );
 
    //   } catch (error) {
    //     console.log(error);
    //     }
      }
    



    return (
        <Box sx={{ display: "flex" }}>
            <SideNav />
            <div
                className="flex flex-col space-y-20 justify-center"
                style={{
                    backgroundColor: colorScheme.background,
                    height: "100vh",
                    width: "100vw",
                    paddingTop: "64px",
                }}
            >
                <Box>
                    <div className="flex items-center justify-center">
                        <FileDropBox>
                            <div className="flex flex-row  uploadText justify-between">
                                <p>Upload</p>
                                <div > 
                                <Button
                                        variant="contained"
                                        endIcon={<SendIcon />}
                                        sx={{
                                        backgroundColor: 'rgba(2, 2, 227, var(--tw-text-opacity))',
                                        
                                        }}
                                        onClick={handleClonecontrolOpen}
                                    >
                                        Clone From GitHub
                                </Button>
                                <Dialog open={openSourcecontrol} onClose={handleClonecontrolClose}>
                                    <DialogTitle>Clone Repositories</DialogTitle>
                                    <DialogContent>
                                    <DialogContentText>
                                        To Clone github repository, please enter repository address here. 
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
                                
                                </div>

                              
                            </div>
                            

                           
                            <div className="files flex mt-4 p-5 justify-between">
                                <div className="flex items-center w-full">
                                    <StyledTextField
                                        className="project-label"
                                        required
                                        label="Project Name"
                                        helperText={projectHelper}
                                        variant="filled"
                                        value={projectName}
                                        onChange={(event) => {
                                            setProjectName(event.target.value);
                                            setProjectHelper("");
                                        }}
                                        sx={{
                                            ".css-4ttn6k-MuiFormHelperText-root": {
                                                color: "red",
                                            },
                                        }}
                                    />
                                </div>
                            </div>
                            <div
                                className="flex flex-col justify-center items-center py-10 dropBox"
                                onDrop={handleDrop}
                                onDragOver={handleDragOver}
                            >
                                <div className="file-arrow-up-solid-1">
                                    <FileEarmarkArrowUpFill />
                                </div>
                                <div className="flex">
                                    <p>Drop your file(s) here or</p>

                                    <div className="browse" onClick={handleBrowse}>
                                        <p> browse</p>
                                        <input
                                            ref={fileInputRef}
                                            type="file"
                                            multiple
                                            style={{ display: "none" }}
                                            onChange={handleInputChange}
                                        />
                                    </div>
                                </div>
                                <p className="max-file-size-25-mb">Max. file size: 25MB</p>
                                <p id="file-error" style={{ color: "red", display: "none" }}>
                                    File must be required*
                                </p>
                            </div>

                            <div className="flex flex-col fileList mt-8">
                                {droppedFiles.map((file, index) => (
                                    <div
                                        key={index}
                                        className="files flex mt-4 p-5 justify-between"
                                    >
                                        <div className="flex items-center">
                                            <File className="file-pdf-regular-1" />
                                            <div className="items-start flex flex-col ml-2">
                                                <p className="fileName1">{file.name}</p>
                                                <p className="fileSize">{file.size} bytes</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center">
                                            <IconButton
                                                className="iconButton"
                                                onClick={() => handleRemoveFile(file)}
                                            >
                                                <Close className="x-solid" />
                                            </IconButton>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <Button
                                className="continue mt-8 p-2 mb-5"
                                onClick={handleRequired}
                            >
                                <p className="continueText">Continue</p>
                            </Button>
                        </FileDropBox>
                    </div>
                </Box>
            </div>
        </Box>
    );
}
