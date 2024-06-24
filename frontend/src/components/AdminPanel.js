// src/pages/AdminPanel.js
import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import axios from 'axios';

const AdminPanel = () => {
  const [newAdmin, setNewAdmin] = useState({ email: '', password: '' });
  const { user } = useAuth();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewAdmin({ ...newAdmin, [name]: value });
  };

  const handleAddAdmin = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:5000/admin/register', newAdmin);
      alert('New admin added successfully');
      setNewAdmin({ email: '', password: '' });
    } catch (error) {
      console.error(error);
      alert('Error adding new admin');
    }
  };

  return (
    <div>
      <h1>Welcome, {user?.email}</h1>
      <h2>Add New Administrator</h2>
      <form onSubmit={handleAddAdmin}>
        <input
          type="email"
          name="email"
          value={newAdmin.email}
          onChange={handleChange}
          placeholder="Email"
          required
        />
        <input
          type="password"
          name="password"
          value={newAdmin.password}
          onChange={handleChange}
          placeholder="Password"
          required
        />
        <button type="submit">Add Admin</button>
      </form>
    </div>
  );
};

export default AdminPanel;
