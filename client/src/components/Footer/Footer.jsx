import React from 'react'
import "./Footer.css"

function Footer() {
  return (
    <div className='footer' id='footer'>
      <div className="footer-content">
        <div className="footer-content-left">
            <img src="https://cdn-icons-png.flaticon.com/256/8327/8327728.png" alt=''/>
            <p>a coin a day keeps poverty away</p>
        </div>
        <div className="footer-content-center">
            <h2>COMPANY</h2>
            <ul>
                <li>Home</li>
                <li>Bills</li>
                <li>Categories</li>
                <li>Payments</li>
            </ul>
        </div>
        <div className="footer-content-right">
            <h2>GET IN TOUCH</h2>
            <ul>
                <li>+254 700 000 111</li>
                <li>contact@budget.com</li>
            </ul>
        </div>
      </div>
      <hr/>
      <p className='footer-copyright'>Copyright 2024 @ Budget.com - All Right Reserved </p>
    </div>
  )
}

export default Footer

