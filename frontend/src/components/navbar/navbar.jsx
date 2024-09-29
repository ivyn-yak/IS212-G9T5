import React from 'react';
import './navbar.css';
import { useLocation } from "react-router-dom";
import attendifyLogo from '../../assets/logo/attendify.png';

import dayjs from 'dayjs';

// Import 'advancedFormat' plugin to display full month names
import localizedFormat from 'dayjs/plugin/localizedFormat';
dayjs.extend(localizedFormat);


function Navbar() {
  return (
    <div className="navbar">
      <div className="navbar-logo">
        <img src={attendifyLogo} alt="Attendify Logo" className="logo" />
      </div>      

      {/* Always show Profile Button */}
      <div className="profile-button">
        <button>Profile</button>
      </div>
      
    </div>
  );
}

export default Navbar;

