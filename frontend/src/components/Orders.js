// src/pages/Orders.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Orders = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/orders');
        setOrders(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div>
      <h1>All Orders</h1>
      <ul>
        {orders.map(order => (
          <li key={order.id}>
            Order ID: {order.id}, Customer: {order.customer}, Total: {order.total}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Orders;
