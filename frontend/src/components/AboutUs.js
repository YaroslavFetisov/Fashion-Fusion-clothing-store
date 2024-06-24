import React from 'react';
import './AboutUs.css';

function AboutUs() {
  return (
    <div className="aboutContainer">
      <div className="aboutTextBox">
        <h1 className="exploreText">
          LET'S<br />
          EXPLORE<br />
          <span className="highlight">UNIQUE</span><br />
          CLOTHES.
        </h1>
      </div>
      <div className="aboutContent">
        <h1 className="aboutTitle">ABOUT US</h1>
        <p>Welcome to Fashion Fusion! At Fashion Fusion, we believe in the power of fashion to express individuality and boost confidence. Our mission is to provide a seamless and enjoyable shopping experience, offering a wide range of stylish clothing and accessories for women, men, and children. We curate our collection to include the latest trends and timeless classics, ensuring that our customers always have access to high-quality, fashionable items.</p>
        
        <h2 className="sectionTitle">WHAT WE OFFER</h2>
        <ul>
          <li><strong>Diverse Selection:</strong> We offer a wide variety of products to cater to different tastes and styles.</li>
          <li><strong>User-Friendly Platform:</strong> Our website is designed to make shopping easy and enjoyable, with features like product search, filtering options, and personalized wish lists.</li>
          <li><strong>Secure Shopping:</strong> We prioritize the security of your personal information and payment details.</li>
          <li><strong>Excellent Customer Service:</strong> Our team is dedicated to providing you with the best shopping experience possible. If you have any questions or need assistance, we're here to help.</li>
        </ul>
        
        <h2 className="sectionTitle">CONTACT US</h2>
        <p>We value your feedback and are here to assist you with any inquiries or concerns.</p>
        <p><strong>Email:</strong> support@fashionfusion.com<br />
           <strong>Phone:</strong> +380(95)-100-100-10<br />
           <strong>Address:</strong> Hryhoriya Skovorody St, 2, Kyiv, 04655</p>
      </div>
    </div>
  );
}

export default AboutUs;
