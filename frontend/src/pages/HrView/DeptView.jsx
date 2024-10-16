import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Box, Button, Drawer, Typography, IconButton } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import dayjs from 'dayjs';

const mockEmployeeData = [
  { staff_id: 101, name: 'Alice Smith', dept: 'Sales', manager_id: 101 },
  { staff_id: 102, name: 'Bob Johnson', dept: 'Engineering', manager_id: 102 },
  { staff_id: 103, name: 'Charlie Brown', dept: 'Sales', manager_id: 101 },
  { staff_id: 104, name: 'David Lee', dept: 'Engineering', manager_id: 101 },
  // More employees...
];

const mockWFHScheduleData = [
  { staff_id: 101, specific_date: '2024-10-14', is_am: true, is_pm: false },
  { staff_id: 102, specific_date: '2024-10-14', is_am: false, is_pm: true },
  // More schedule entries...
];

// Helper function to get staff name by ID
const getStaffName = (staffID) => {
  const staff = mockEmployeeData.find(person => person.staff_id === staffID);
  return staff ? staff.name : 'Unknown';
};

// Helper function to get employees by team (manager_id)
const getTeamMembers = (managerID) => {
  return mockEmployeeData.filter(employee => employee.manager_id === managerID);
};

const DeptView = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { department, date } = location.state || {}; // Retrieve department and date from passed state
  const [selectedTeam, setSelectedTeam] = useState(null);

  // Filter employees by department
  const departmentTeams = [...new Set(mockEmployeeData
    .filter(emp => emp.dept === department)
    .map(emp => emp.manager_id))];

  const handleTeamClick = (manager_id) => {
    const teamMembers = getTeamMembers(manager_id);
    setSelectedTeam(teamMembers);
  };

  const handleClose = () => {
    setSelectedTeam(null);
  };

  // Check if date is a valid object, if not fallback to current date
  const displayDate = date ? dayjs(date) : dayjs();

  return (
    <Box p={2}>
      <Box display="flex" alignItems="center" mb={2}>
        <IconButton onClick={() => navigate('/hr/hr-calendar')} style={{ marginRight: '16px' }}>
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h4">
          {department} - {displayDate.format('MMM D, YYYY')}
        </Typography>
      </Box>

      {/* Display Teams in the Department */}
      {departmentTeams.length ? (
        <Box display="flex" flexWrap="wrap" gap={2}>
          {departmentTeams.map((managerID, index) => (
            <Button
              key={index}
              variant="outlined"
              onClick={() => handleTeamClick(managerID)}
              style={{ width: '150px', height: '100px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}
            >
              <Typography variant="h6">{`Team managed by ${getStaffName(managerID)}`}</Typography>
              <Typography>Members: {getTeamMembers(managerID).length}</Typography>
            </Button>
          ))}
        </Box>
      ) : (
        <Typography>No teams available for the selected department.</Typography>
      )}

      {/* Drawer to Show Team Members Working from Office/Home */}
      <Drawer anchor="right" open={Boolean(selectedTeam)} onClose={handleClose}>
        <Box p={2} width={250}>
          {selectedTeam && (
            <>
              <Typography variant="h6">Team Members</Typography>
              {selectedTeam.map((staffMember, index) => (
                <Box key={index} mb={2}>
                  <Typography variant="subtitle1">{getStaffName(staffMember.staff_id)}</Typography>
                  {mockWFHScheduleData
                    .filter(schedule => schedule.staff_id === staffMember.staff_id)
                    .map((schedule, i) => (
                      <Typography key={i} variant="body2">
                        {`Date: ${dayjs(schedule.specific_date).format('MMM D, YYYY')} - AM: ${schedule.is_am ? 'In Office' : 'Remote'}, PM: ${schedule.is_pm ? 'In Office' : 'Remote'}`}
                      </Typography>
                  ))}
                </Box>
              ))}
            </>
          )}
        </Box>
      </Drawer>
    </Box>
  );
};

export default DeptView;







