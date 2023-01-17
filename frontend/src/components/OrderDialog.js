import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function OrderDialog(props) {
  const [open, setOpen] = React.useState(false);
  const {buttonTitle, dialogTitle, contentText, update } = props;

  const inputStyleShort = { marginRight:5, marginLeft:5, width:60 };
  const inputStyle = { marginRight:5, marginLeft:5 };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    let orderId = 1;
    if (update) {
     orderId = event.target.querySelector(
        'input[name="id"]').value;    }
    let orderName = event.target.querySelector(
        'input[name="name"]').value;
    let value = event.target.querySelector(
        'input[name="value"]').value;
    let weight = event.target.querySelector(
        'input[name="weight"]').value;
    if (orderName && value && weight && orderId) {
    let order = [{
        id: orderId,
        name: orderName,
        weight: weight,
        value: value
        }];
    props.onClick(order);
    setOpen(false);
    } else {
        alert('At least one field left empty. Cancelling.')
    }
    setOpen(false);
  }

  return (
    <div>
      <Button style={{marginRight:10, marginLeft:10}} variant="outlined" onClick={handleClickOpen}>
        {buttonTitle}
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{dialogTitle}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {contentText}
          </DialogContentText>
          <div>
          <form action="#" onSubmit={handleSubmit}>
          {update && <input style={inputStyleShort} type= "number" name="id" id="id" placeholder="id" required/>  }
          <input style={inputStyle} type="text" name="name" id="name" placeholder="name" required />  
          <input style={inputStyleShort} type= "number" min="0" max="99999" name="value" id="value" placeholder="value" required />  
          <input style={inputStyleShort} type= "number" min="0" max="100" name="weight" id="weight" placeholder="weight" required />
          <input style={inputStyleShort} type="submit" />
          </form>
          </div>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}