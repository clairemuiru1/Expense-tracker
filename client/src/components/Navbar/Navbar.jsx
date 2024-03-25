import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRightFromBracket } from '@fortawesome/free-solid-svg-icons';
import './Navbar.css';

function Navbar({ setShowLogin }) { 
  return (
    <div className='navbar'>
      <img src='https://cdn-icons-png.flaticon.com/512/3322/3322850.png' alt='logo' className='logo' />
      <ul className="navbar-menu">
        <li>Home</li>
        <li>Bills</li>
        <li>Categories</li>
        <li>Payments</li>
      </ul>
      <div className='navbar-right'>
        <FontAwesomeIcon icon={faRightFromBracket} className='logout' />
        <button onClick={() => setShowLogin(true)}>Sign In</button>
      </div>
    </div>
  );
}

export default Navbar;
