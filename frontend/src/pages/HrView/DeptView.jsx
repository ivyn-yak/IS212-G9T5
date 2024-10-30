import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Button, Typography, Box, Card, List, ListItem, ListItemText } from '@mui/material';

const DeptView = () => {
  const location = useLocation();
  const { department, date } = location.state;
  const [view, setView] = useState('dept'); // 'dept' for department view, 'team' for team view
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [teams, setTeams] = useState([]);
  const [teamMembers, setTeamMembers] = useState([]);
  const [availableEmployees, setAvailableEmployees] = useState([]);

  // Fetch all employees and set up teams within the department
  const fetchEmployeeData = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/all', { credentials: 'include' });
      if (!response.ok) {
        throw new Error('Failed to fetch employee data');
      }

      const employeeData = await response.json();
      setAvailableEmployees(employeeData);

      // Filter managers by department and set up teams
      const deptManagers = employeeData
        .filter(employee => employee.role === 3 && employee.dept.toLowerCase() === department.toLowerCase())
        .map(manager => ({
          teamName: `Team of ${manager.staff_fname} ${manager.staff_lname}`,
          managerId: manager.staff_id,
          members: employeeData.filter(emp => emp.reporting_manager === manager.staff_id)
        }));

      setTeams(deptManagers);
    } catch (error) {
      console.error('Error fetching employee data:', error);
    }
  };

  useEffect(() => {
    if (view === 'dept') {
      fetchEmployeeData();
    }
  }, [view, department]);

  // Fetch team members for the selected team and date
  useEffect(() => {
    if (view === 'team' && selectedTeam) {
      const fetchTeamSchedule = async () => {
        try {
          const response = await fetch(`http://localhost:5001/api/manager/${selectedTeam.managerId}/team_schedule?start_date=${date}&end_date=${date}`);
          const data = await response.json();

          if (data.team) {
            setTeamMembers(data.team.map(member => ({
              staffId: member.staff_id,
              inOffice: member.ScheduleDetails.length === 0 // Assume in-office if no WFH schedule details for that date
            })));
          }
        } catch (error) {
          console.error('Error fetching team schedule:', error);
        }
      };

      fetchTeamSchedule();
    }
  }, [view, selectedTeam, date]);

  // Handler to view a specific team
  const handleTeamClick = (team) => {
    setSelectedTeam(team);
    setView('team');
  };

  // Handler to go back to department view
  const handleBackClick = () => {
    setView('dept');
    setSelectedTeam(null);
  };

  return (
    <div>
      {view === 'dept' ? (
        // Department View: Show list of teams in the department
        <div>
          <Typography variant="h4" gutterBottom>{`Department: ${department}`}</Typography>
          <Typography variant="h6">{`Date: ${date}`}</Typography>
          <Box mt={3}>
            {teams.map((team) => (
              <Card key={team.managerId} style={{ marginBottom: '16px', padding: '16px' }}>
                <Typography variant="h6">{team.teamName}</Typography>
                <Button variant="outlined" onClick={() => handleTeamClick(team)}>
                  View Team
                </Button>
              </Card>
            ))}
          </Box>
        </div>
      ) : (
        // Team View: Show team members' attendance
        <div>
          <Button variant="contained" color="primary" onClick={handleBackClick}>
            Back to Department View
          </Button>
          <Typography variant="h4" gutterBottom>{`Team: ${selectedTeam.teamName}`}</Typography>
          <Typography variant="h6">{`Date: ${date}`}</Typography>
          <Box mt={3}>
            <List>
              {teamMembers.map((member, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`Staff ID: ${member.staffId}`}
                    secondary={member.inOffice ? 'In Office' : 'Working From Home'}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        </div>
      )}
    </div>
  );
};

export default DeptView;










