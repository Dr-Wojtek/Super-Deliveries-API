import React, {useEffect, useState} from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export function RenderMap(props) {
    const { addresses, orders, results } = props;
    const [addressInfo, setAddressInfo] = useState({})
    const [open, setOpen] = useState(false);
    const [cityMap, setCityMap] = useState(null);
   useEffect(() => {
        let max_x = 0
        let min_x = Infinity
        let min_y = Infinity
        let max_y = 0
        let x_range = []
        let y_range = []
        addresses.forEach(address => {
        if (address.coordinate_x > max_x){max_x = address.coordinate_x;}
        if (address.coordinate_x < min_x){min_x = address.coordinate_x;}
        if (address.coordinate_y > max_y){max_y = address.coordinate_y;}
        if (address.coordinate_y < min_y){min_y = address.coordinate_y;}                                  
        })
        for (let x = min_x; x <= max_x; x++) {x_range.push(x);}
        for (let y = min_y; y <= max_y; y++) {y_range.push(y);}
        let temp_map = Array(y_range.length).fill().map(row => Array(x_range.length).fill());
        addresses.forEach(address => {
        let row = y_range.indexOf(address.coordinate_y);
        let col = x_range.indexOf(address.coordinate_x);
        temp_map[row][col] = {"name":address.name, "id": address.id, "adj1":address.adj1, adj1_d:address.adj1_distance,
        "adj2":address.adj2, adj2_d:address.adj2_distance,"adj3":address.adj3, adj3_d:address.adj3_distance,
        "adj4":address.adj4, adj4_d:address.adj4_distance};
        })
        if (results) {
            let stops = [];
            let route = [];
            let path = results.final_path;
            for (let i = 2; i < path.length; i++){
              if (path[i] === path[i-1]){
                stops.push(path[i]);
              }
              if (path[i] !== path[i-1]) {
                route.push(path[i]);
              }
            }
            temp_map.map(row => {row.map(address => {
              if (address.name === results.logistics_office) {
                address.style = { backgroundColor: `rgba(${255}, ${255}, ${0}, ${1})` };
                address.order = "(Logistics Office)";
              }
              else if (route.includes(address.name)) {
                let position = route.indexOf(address.name) +1;
                address.style = { backgroundColor: `rgba(${255-(position*7)}, ${255}, ${0}, ${1})`, transition: "background-color 2s" };
              }
              if (stops.includes(address.name)){
                address.stop = "( " + (stops.indexOf(address.name)+1) + " )";
                for (let i = 0; i < orders.length; i++) {
                  if (orders[i].address === address.id) {
                    address.order = "(" + orders[i].name +")";
                  }
                }
              }
             
            })})
        }
        setCityMap(temp_map);
    }, [results])

    const renderRow = address => {
        return (
          <td style={address.style} key={address.name} onClick={
            () => { setAddressInfo(address);
                    setOpen(true) }} >
            <p className="stop">{address.stop}</p>
            <p className="address">{address.name}</p>            
            <p className="order">{address.order}</p>
            </td>
          )
        }
    
    const PopupInfo = () => {
        return (
        <div classname="map">
        <Dialog
          open={open}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description">
          <DialogTitle id="alert-dialog-title">
          {addressInfo.name}
          </DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              {`Connections:`}<br/>
              {addressInfo.adj1 && `${addressInfo.adj1}, ${addressInfo.adj1_d} km`}<br/>
              {addressInfo.adj2 && `${addressInfo.adj2}, ${addressInfo.adj2_d} km`}<br/> 
              {addressInfo.adj3 && `${addressInfo.adj3}, ${addressInfo.adj3_d} km`}<br/>
              {addressInfo.adj4 && `${addressInfo.adj4}, ${addressInfo.adj4_d} km`}      
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} autoFocus>
              OK
            </Button>
          </DialogActions>
        </Dialog>
        </div>
        );
    }
    
    const handleClose = () => {
        setOpen(false);
        };

    if (!cityMap) {
    return <div><h1> City map is loading... </h1></div>;
  }  
     return (
      <div>
      <PopupInfo />
          <table className="addresses">
          <tbody>            
            {cityMap.slice(0, cityMap.length).map((address, index) => {
              return (
                <tr key={index}>
                  {renderRow(address[0])}{renderRow(address[1])}{renderRow(address[2])}{renderRow(address[3])}
                  {renderRow(address[4])}{renderRow(address[5])}{renderRow(address[6])}{renderRow(address[7])}
                  {renderRow(address[8])}{renderRow(address[9])}
                </tr>
                )
              })}
          </tbody>
          </table>
          </div>
            );
  }