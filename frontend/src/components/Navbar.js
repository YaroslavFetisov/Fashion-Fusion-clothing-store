// src/components/Navbar.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleProtectedClick = (path) => {
    if (!user) {
      alert('You must be logged in to view this page.');
      navigate('/login');
    } else {
      navigate(path);
    }
  };

  return (
    <nav className="navbar">
      <Link to="/" className="nav-logo">FASHION</Link>
      <div className="nav-links">
        <Link to="/catalogue">CATALOGUE</Link>
        <Link to="/about-us">ABOUT US</Link>
        {user ? (
          user.role === 'admin' ? (
            <>
              <Link to="/admin-panel">ADMIN PANEL</Link>
              <Link to="/orders">ORDERS</Link>
              <Link to="#" onClick={handleLogout}>SIGN OUT</Link>
            </>
          ) : (
            <>
              <Link to="/my-account">MY ACCOUNT</Link>
              <Link to="/cart">CART</Link>
              <Link to="#" onClick={handleLogout}>SIGN OUT</Link>
            </>
          )
        ) : (
          <>
            <Link to="/login">LOG IN</Link>
            <Link to="/register">REGISTER</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
