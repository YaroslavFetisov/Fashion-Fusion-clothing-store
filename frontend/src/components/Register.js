// src/pages/Register.js
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from './AuthContext';
import './Login.css';

function Register() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const validatePassword = (password) => {
    const re = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}$/;
    return re.test(password);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (email.length > 50 || !validateEmail(email)) {
      setError('Email must be valid and up to 50 characters');
      return;
    }
    if (password.length < 8 || password.length > 16 || !validatePassword(password)) {
      setError('Password must be 8-16 characters long, include Latin characters, numbers, and capital letters');
      return;
    }
    if (password !== repeatPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/customer/register', {
        firstName,
        lastName,
        email,
        password,
        address: 'dummy address'  // Replace with actual address field if needed
      });
      if (response.status === 201) {
        login(response.data.user);
        setSuccess('Registration successful! Redirecting to home...');
        setTimeout(() => {
          navigate('/');
        }, 2000);
      }
    } catch (error) {
      if (error.response && error.response.data) {
        setError(error.response.data.message);
      } else {
        setError('An unexpected error occurred');
      }
    }
  };

  return (
    <div className="container">
      <div className="loginBox">
        <h1 className="loginText">REGISTRATION</h1>
        {error && (
          <div className="alert">
            <span className="closebtn" onClick={() => setError('')}>&times;</span>
            {error}
          </div>
        )}
        {success && (
          <div className="success">
            {success}
          </div>
        )}
        <form onSubmit={handleSubmit}>
          <h2 className="contactInfo">CONTACT INFO</h2>
          <input
            type="text"
            placeholder="First Name"
            className="input"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Last Name"
            className="input"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            required
          />
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
          <p className="passwordInfo">
            Password must contain 8-16 symbols, include Latin small and capital letters, and at least 1 number
          </p>
          <input
            type="password"
            placeholder="Repeat Password"
            className="input"
            value={repeatPassword}
            onChange={(e) => setRepeatPassword(e.target.value)}
            required
          />
          <div className="registerContainer">
            <span>Have an account yet? </span>
            <Link to="/login" className="signUpLink">Log in</Link>
          </div>
          <button type="submit" className="loginButton">Sign up</button>
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

export default Register;
