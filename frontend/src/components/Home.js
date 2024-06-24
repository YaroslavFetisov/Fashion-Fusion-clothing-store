import React from 'react';
import { useAuth } from './AuthContext';
import './Home.css';

const Home = () => {
  const { user } = useAuth();

  return (
    <div className="home-page">
      <div className="home-banner">
        <h1>LET'S EXPLORE UNIQUE CLOTHES.</h1>
        <button className="shop-now">Shop Now</button>
      </div>
    </div>
  );
}

export default Home;
