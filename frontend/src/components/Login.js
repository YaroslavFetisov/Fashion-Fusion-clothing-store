// src/pages/Login.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from './AuthContext';
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/auth/login', { email, password });
      login(response.data.user);
      navigate('/'); // Redirect to home after login
    } catch (error) {
      setError('Invalid email or password');
    }
  };

  return (
    <div className="container">
      <div className="loginBox">
        <h1 className="loginText">LOGIN</h1>
        {error && <div className="alert">{error}</div>}
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            className="input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <div className="registerContainer">
            <span>Don't have an account? </span>
            <Link to="/register" className="signUpLink">Sign up</Link>
          </div>
          <button type="submit" className="loginButton">Log in</button>
        </form>
      </div>
      <div className="exploreBox">
        <h1 className="exploreText">
          LET'S<br />
          EXPLORE<br />
          <span className="highlight">UNIQUE</span><br />
          CLOTHES.
        </h1>
      </div>
    </div>
  );
}

export default Login;
