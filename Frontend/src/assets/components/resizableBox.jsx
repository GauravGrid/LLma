import React, { useState } from "react";
import Draggable from "react-draggable";
import {
  Button,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Paper
} from "@mui/material";
import { styled } from '@mui/material/styles';
import { ResizableBox } from "react-resizable";

const ResizablePaper = styled(Paper)(({ theme }) => ({
  position: "relative",
  "& .react-resizable-handle": {
    position: "absolute",
    width: 20,
    height: 20,
    bottom: 0,
    right: 0,
    background:
      "url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2IDYiIHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOiNmZmZmZmYwMCIgeD0iMHB4IiB5PSIwcHgiIHdpZHRoPSI2cHgiIGhlaWdodD0iNnB4Ij48ZyBvcGFjaXR5PSIwLjMwMiI+PHBhdGggZD0iTSA2IDYgTCAwIDYgTCAwIDQuMiBMIDQgNC4yIEwgNC4yIDQuMiBMIDQuMiAwIEwgNiAwIEwgNiA2IEwgNiA2IFoiIGZpbGw9IiMwMDAwMDAiLz48L2c+PC9zdmc+')",
    backgroundPosition: "bottom right",
    padding: "0 3px 3px 0",
    backgroundRepeat: "no-repeat",
    backgroundOrigin: "content-box",
    boxSizing: "border-box",
    cursor: "se-resize"
  }
}));

const DraggableResizableDialog = () => {
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button onClick={handleClickOpen}>Open dd form dialog</Button>
      {open && (
        <Dialog
          open={true}
          onClose={handleClose}
          maxWidth={false}
          PaperComponent={ResizablePaper}
          aria-labelledby="draggable-dialog-title"
        >
          <ResizableBox height={400} width={600}>
            <div>
              <DialogTitle style={{ cursor: 'move' }} id="draggable-dialog-title">Subscribe</DialogTitle>
              <DialogContent>
                <DialogContentText>
                  To subscribe to this website, please enter your email address here.
                  We will send updates occasionally.
                </DialogContentText>
                <TextField
                  autoFocus
                  margin="dense"
                  id="name"
                  label="Email Address"
                  type="email"
                  fullWidth
                />
              </DialogContent>
              <DialogActions>
                <Button onClick={handleClose} color="primary">
                  Cancel
                </Button>
                <Button onClick={handleClose} color="primary">
                  Subscribe
                </Button>
              </DialogActions>
            </div>
          </ResizableBox>
        </Dialog>
      )}
    </div>
  );
};

export default DraggableResizableDialog;
