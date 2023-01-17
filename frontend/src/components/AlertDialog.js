import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function AlertDialog(props) {
  const [open, setOpen] = React.useState(false);
  const {buttonTitle, dialogTitle, contentText, label, onClick } = props;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleCloseGo = () => {
    setOpen(false);
    onClick();
    };

  return (
    <div>
      <Button variant="outlined" onClick={handleClickOpen} style={{ marginRight:10, marginLeft:10 }}>
      {buttonTitle}
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
            {dialogTitle}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {contentText}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleCloseGo} autoFocus>
            Apply
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}