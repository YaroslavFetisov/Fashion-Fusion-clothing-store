// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import { AuthProvider } from './components/AuthContext';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Catalogue from './components/Catalogue';
import AboutUs from './components/AboutUs';
import AdminPanel from './components/AdminPanel';
import Orders from './components/Orders';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/catalogue" element={<Catalogue />} />
          <Route path="/about-us" element={<AboutUs />} />
          <Route path="/admin-panel" element={<AdminPanel />} />
          <Route path="/orders" element={<Orders />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
