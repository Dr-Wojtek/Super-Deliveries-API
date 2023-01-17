import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function FormDialog(props) {
  const [open, setOpen] = React.useState(false);
  const [value, setValue] = React.useState(null);
  const {buttonTitle, dialogTitle, contentText, label, onClose } = props;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    if (value) {
    onClose(value);
    setValue(null);
    }
  };
  
  const handleChange = event => {
    event.preventDefault();
    setValue(event.target.value);
  }

  return (
    <div>
      <Button style={{ marginRight:10, marginLeft:10 }} variant="outlined" onClick={handleClickOpen}>
        {buttonTitle}
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{dialogTitle}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {contentText}
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            type="number"
            min="1"
            max="99"
            id="name"
            label={label}
            fullWidth
            variant="standard"
            onChange={handleChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>OK</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}