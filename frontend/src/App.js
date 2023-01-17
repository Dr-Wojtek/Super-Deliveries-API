import React, { useState, useEffect } from 'react';
import './App.css';
import { RenderMap } from './components/RenderMap.js';
import { RenderOrders } from './components/RenderOrders.js';
import FormDialog from './components/FormDialog.js';
import OrderDialog from './components/OrderDialog';
import ContainedButtons from './components/ContainedButton.js'
import {RenderInfo} from './components/RenderInfo.js'
import AlertDialog from './components/AlertDialog';
import Bottom from './components/Bottom.js'

function App() {
  const [addresses, setAddresses] = useState(null);
  useEffect(() => {
    let fetchData = async () => {
    let response = await fetch(`${domainAddress}/addresses`);
    let json = await response.json();
    setAddresses(json);
    }
    fetchData()    
    .catch(console.error);;   
    }, [])
  const [ results, setResults ] = useState();
  const [ orders, setOrders ] = useState(null);
  const domainAddress = "https://alexstrae.eu.pythonanywhere.com";

  const getOrders = () => {
    let fetchData = async () => {
    let response = await fetch(`${domainAddress}/orders`);
    let json = await response.json();
    setOrders(json);
    }
    fetchData()
    .catch(console.error);
  }

  const addOrder = order => {
    let fetchData = async () => {
      let requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(order)
      };
      fetch(`${domainAddress}/orders`, requestOptions);  
    }
    fetchData()
    .catch(console.error);
    setTimeout(getOrders, 1000);
  }

  const updateOrder = order => {
    let fetchData = async () => {
      let requestOptions = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(order)
      };
      fetch(`${domainAddress}/orders`, requestOptions);
    }
    fetchData()
    .catch(console.error);
    setTimeout(getOrders, 1000);
  }

  const deleteOrder = id => {
    let fetchData = async () => {
      fetch(`${domainAddress}/orders/${id}`, {method: 'DELETE'});
    }
    fetchData()
    .catch(console.error);
    setTimeout(getOrders, 1000);
  }

  const setWeightLimit = limit => {
    let fetchData = async () => {
      let requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orders)
      };
      let response = await fetch(`${domainAddress}/limitingFactor/${limit}`, requestOptions);
      let json = await response.json();
      setOrders(json);
    }
    fetchData()
    .catch(console.error);
    }

  const getResults = () => {  
    let fetchData = async () => {
      let requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orders)
      };
      let response = await fetch(`${domainAddress}/getRoute`, requestOptions);
      let json = await response.json();
      setResults(json);
      }
      fetchData();  
  }

  const resetOrders = () => {
    let fetchData = async () => {
      fetch(`${domainAddress}/resetOrders`, {method: 'DELETE'});
    }
    fetchData();
    setTimeout(getOrders, 1000);
  }

  return (
    <div>
      <div className="title">
        <h1 className="title">Super Deliveries</h1>
        <p className="title">Fast delivery routes in Stockholm</p>
      </div>
      <div className="actions">
        <ContainedButtons onClick={getOrders} value='Get Orders' />
        <OrderDialog onClick={addOrder} buttonTitle="Add order" dialogTitle="Add a custom order"/>
        <OrderDialog onClick={updateOrder} update={true} buttonTitle="Update order" dialogTitle="Update a custom order"/>
        <FormDialog onClose={deleteOrder} buttonTitle="Delete order" dialogTitle="Delete an order" contentText="Enter id to delete" label="#id"/>
      </div>
      {orders && <RenderOrders orders={orders} />}
      <div className="actions">
        {orders && <ContainedButtons onClick={getResults} value='Run Delivery Trip'/>}  
        {orders && <FormDialog onClose={setWeightLimit} buttonTitle="Set delivery weight limit" dialogTitle="Apply weight limit" 
        contentText="Filter the most valuable orders within this weight" label="weight in kg"/>}
        {orders && <AlertDialog onClick={resetOrders} buttonTitle="Reset order list" dialogTitle="Reset default order list?" contentText="Custom orders will be lost."/>}
      </div>
      <br/>
      {addresses && <RenderMap addresses={addresses} orders={orders} results={results}/>}
      {results && <RenderInfo results={results}/>}
      <br/>
      <br/>
      <br/>
      <Bottom />
    </div>
    );
      }
    
export default App;