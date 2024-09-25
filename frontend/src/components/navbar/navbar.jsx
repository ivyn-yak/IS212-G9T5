import React from 'react';
import './navbar.css';
import { useLocation } from "react-router-dom";
import attendifyLogo from '../../assets/logo/attendify.png';
import { TextField, InputAdornment, Button, IconButton } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

import dayjs from 'dayjs';

// Import 'advancedFormat' plugin to display full month names
import localizedFormat from 'dayjs/plugin/localizedFormat';
dayjs.extend(localizedFormat);


function Navbar() {
  const location = useLocation();

  // Routes where the search bar SHOULD be shown
  const haveSearchRoutes = ["/"];
  const haveDateSelector = ["/"];

  // Determine whether to show the search bar
  const showSearch = haveSearchRoutes.some((route) =>
    location.pathname.startsWith(route)
  );

  const showDateSelector = haveDateSelector.some((route) =>
    location.pathname.startsWith(route)
  );
  
  return (
    <div className="navbar">
      <div className="navbar-logo">
        <img src={attendifyLogo} alt="Attendify Logo" className="logo" />
      </div>
      {/* Conditionally show Date Selector */}
      <div className="buttons">
        
      {showDateSelector && (
        <>
          <Button variant="outlined">
            Today
          </Button>

          <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DemoContainer components={['DatePicker']}>
            <DatePicker 
              label={dayjs().format('MMMM D')}  // Display as "July 17"
            />
          </DemoContainer>
        </LocalizationProvider>
        </>
      )}
        
        {/* Conditionally show Search */}
        {showSearch && (
            <TextField
              variant="outlined"
              placeholder="Search..."
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
              style={{ width: '300px' }} // Adjust the width as necessary
            />
        )}

        {showDateSelector && (
        /* Arrows for Navigation */
          <div style={{ display: 'flex', alignItems: 'center', marginLeft: '10px' }}>
            <IconButton>
              <ArrowBackIcon />
            </IconButton>
            <IconButton>
              <ArrowForwardIcon />
            </IconButton>
          </div>
        )}
      </div>

      {/* Always show Profile Button */}
      <div className="profile-button">
        <button>Profile</button>
      </div>
      
    </div>
  );
}

export default Navbar;

