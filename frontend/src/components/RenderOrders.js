import React from 'react';

export function RenderOrders(props) {
    const orders = props.orders;

    if (!orders) {
      console.log(orders)
      return <div> Orders are loading...</div>;
    }
    else {
    return  <div className="orders">
    <table className="orders">
   <thead>   
    <tr>
      <th>Id</th>
      <th>Name</th>
      <th>Value</th>
      <th>Weight</th>
      <th>Address ID</th>
    </tr>
  </thead>
  <tbody>
  {orders.map((val, key) => {
    return (
      <tr key={key}>
        <td>{val.id}</td>
        <td>{val.name}</td>
        <td>${val.value}</td>
        <td>{val.weight} kg</td>
        <td>{val.address}</td>
      </tr>
    )
  })}
  </tbody>
  </table>  
    </div>          
    }}
  