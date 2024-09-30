import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Box, Button, Drawer, List, ListItem, ListItemText, Typography, IconButton } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack'; // Import the arrow icon
import dayjs from 'dayjs';  // Make sure dayjs is imported

const mockTeamsData = {
  Sales: [
    { teamName: 'Team A', office: ['2'], home: ['1'] },  // Sept 25
    { teamName: 'Team B', office: ['4'], home: [] },  // Sept 26
    { teamName: 'Team C', office: [], home: ['8', '9'] }  // Sept 27
  ],
  Marketing: [
    { teamName: 'Team A', office: [], home: ['3'] },  // Sept 25
    { teamName: 'Team B', office: ['5'], home: [] }  // Sept 26
  ],
  HR: [
    { teamName: 'Team A', office: ['6'], home: ['7'] },  // Sept 26
    { teamName: 'Team B', office: ['10'], home: [] }  // Sept 27
  ]
};

const mockStaffData = [
  { StaffID: '1', Name: 'John Doe' },
  { StaffID: '2', Name: 'Jane Smith' },
  { StaffID: '3', Name: 'Bob Johnson' },
  { StaffID: '4', Name: 'Alice Brown' },
  { StaffID: '5', Name: 'Emma Watson' },
  { StaffID: '6', Name: 'Clark Kent' },
  { StaffID: '7', Name: 'Diana Prince' },
  { StaffID: '8', Name: 'Chris Evans' },
  { StaffID: '9', Name: 'Mark Ruffalo' },
  { StaffID: '10', Name: 'Bruce Wayne' }
];

// Helper function to get staff name by ID
const getStaffName = (staffID) => {
  const staff = mockStaffData.find(person => person.StaffID === staffID);
  return staff ? staff.Name : 'Unknown';
};

const DeptView = () => {
  const location = useLocation();
  const navigate = useNavigate(); // Define useNavigate as navigate
  const { department, date } = location.state || {}; // Retrieve department and date from passed state
  const [selectedTeam, setSelectedTeam] = useState(null);

  const handleTeamClick = (team) => {
    setSelectedTeam(team);
  };

  const handleClose = () => {
    setSelectedTeam(null);
  };

  // Check if date is a valid object, if not fallback to current date
  const displayDate = date ? dayjs(date) : dayjs();

  const teams = mockTeamsData[department] || [];

  return (
    <Box p={2}>
    
          {/* Back Button with Left Arrow */}
      <Box display="flex" alignItems="center" mb={2}>
        <IconButton 
          onClick={() => navigate('/hr/hr-calendar')} // Navigate back to the calendar page
          style={{ marginRight: '16px' }} // Add spacing
        >
          <ArrowBackIcon /> {/* Arrow icon */}
        </IconButton>

        {/* Display Department Name */}
        <Typography variant="h4">
          {department} - {displayDate.format('MMM D, YYYY')}
        </Typography>
      </Box>


      {/* Display Teams in the Department */}
      <Box display="flex" flexWrap="wrap" gap={2}>
        {teams.map((team, index) => (
          <Button
            key={index}
            variant="outlined"
            onClick={() => handleTeamClick(team)}
            style={{ width: '150px', height: '100px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}
          >
            <Typography variant="h6">{team.teamName}</Typography>
            <Typography>Office: {team.office.length}</Typography>
            <Typography>Home: {team.home.length}</Typography>
          </Button>
        ))}
      </Box>

      {/* Drawer to Show Team Members Working from Office/Home */}
      <Drawer anchor="right" open={Boolean(selectedTeam)} onClose={handleClose}>
        <Box p={2} width={250}>
          {selectedTeam && (
            <>
              <Typography variant="h6">{selectedTeam.teamName}</Typography>
              <Typography variant="subtitle1">Working from Office:</Typography>
              <List>
                {selectedTeam.office.map((personID, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={getStaffName(personID)} /> {/* Get name from ID */}
                  </ListItem>
                ))}
              </List>
              <Typography variant="subtitle1">Working from Home:</Typography>
              <List>
                {selectedTeam.home.map((personID, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={getStaffName(personID)} /> {/* Get name from ID */}
                  </ListItem>
                ))}
              </List>
            </>
          )}
        </Box>
      </Drawer>
    </Box>
  );
};

export default DeptView;



