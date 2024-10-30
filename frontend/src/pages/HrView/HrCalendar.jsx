import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, Card, Typography, IconButton, Button
} from '@mui/material';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

import dayjs from 'dayjs';
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter';
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore';
dayjs.extend(isSameOrAfter);
dayjs.extend(isSameOrBefore);


// Define AttendanceCell component within the same file
const AttendanceCell = ({ date, department, managerIds }) => {
  const [attendance, setAttendance] = useState(null);

  useEffect(() => {
    const fetchAttendance = async () => {
      let inOfficeCount = 0;
      let totalCount = 0;

      for (const managerId of managerIds) {
        try {
          const response = await fetch(`http://localhost:5001/api/manager/${managerId}/team_schedule?start_date=${date}&end_date=${date}`);
          const data = await response.json();

          if (data.team) {
            const inOffice = data.team.reduce((count, member) => {
              const isWFH = member.ScheduleDetails.some(detail => detail.specific_date === date);
              return !isWFH ? count + 1 : count;
            }, 0);

            inOfficeCount += inOffice;
            totalCount += data.team.length;
          }
        } catch (error) {
          console.error(`Error fetching attendance for manager ${managerId} on ${date}:`, error);
        }
      }

      setAttendance({ inOffice: inOfficeCount, total: totalCount });
      console.log(attendance);
    };

    fetchAttendance();
  }, [date, managerIds]);

  return (
    <Card className="schedule-card">
      <Box p={1}>
        {attendance ? (
          <Typography variant="body2">
            {department}: {attendance.inOffice} / {attendance.total}
          </Typography>
        ) : (
          <Typography variant="body2">Loading...</Typography>
        )}
      </Box>
    </Card>
  );
};

// Main HrCalendar component
const HrCalendar = () => {
  const [currentDate, setCurrentDate] = useState(dayjs());
  const [availableEmployees, setAvailableEmployees] = useState([]);
  const [managers, setManagers] = useState([]);
  const navigate = useNavigate();

  const { staffId } = useParams(); // Get staffId and role from URL parameters
  console.log(staffId);
  // console.log(role)

  const handleDepartmentClick = (department, date) => {
    navigate(`/${staffId}/1/dept-view`, { state: { department, date } }); // Use absolute path
  };

  const shifts = [
    { name: 'AM', time: '9:00 - 13:00' },
    { name: 'PM', time: '14:00 - 18:00' }
  ];

  const weekDates = Array.from({ length: 7 }, (_, i) => currentDate.startOf('week').add(i, 'day').format('YYYY-MM-DD'));

  // Fetch employee data and managers with their team sizes
  useEffect(() => {
    const fetchEmployeeData = async () => {
      try {
        const response = await fetch('http://localhost:5001/api/all', { credentials: 'include' });
        if (!response.ok) {
          throw new Error('Failed to fetch employee data');
        }
        
        const employeeData = await response.json();
        setAvailableEmployees(employeeData);
  
        const managerList = employeeData
          .filter(employee => employee.role === 3)
          .reduce((acc, manager) => {
            const department = manager.dept.toLowerCase();
            const teamSize = employeeData.filter(emp => emp.reporting_manager === manager.staff_id).length;
  
            if (!acc[department]) {
              acc[department] = [];
            }
  
            acc[department].push({ 
              staffId: manager.staff_id, 
              teamSize 
            });
            
            return acc;
          }, {});
  
        setManagers(managerList);
      } catch (error) {
        console.error('Error fetching employee data:', error);
      }
    };
  
    fetchEmployeeData();
  }, []);

  const handlePrevWeek = () => {
    setCurrentDate(currentDate.subtract(1, 'week'));
  };

  const handleNextWeek = () => {
    setCurrentDate(currentDate.add(1, 'week'));
  };

  const handleDateChange = (newDate) => {
    setCurrentDate(dayjs(newDate));
  };

  return (
    <div className="weekly-schedule-container">
      <TableContainer component={Paper} className="centered-table-container">
        <Table className="styled-table">
          <TableHead>
            <TableRow>
              <TableCell>Shift</TableCell>
              {weekDates.map((date) => (
                <TableCell key={date}>
                  {date}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {shifts.map(shift => (
              <TableRow key={shift.name}>
                <TableCell className="shift-cell">
                  {shift.name}
                  <br />
                  ({shift.time})
                </TableCell>
                {weekDates.map((date) => (
                  <TableCell key={`${date}-${shift.name}`}>
                    {Object.entries(managers).map(([department, managersList]) => (
                      <Button
                        key={`${date}-${department}`}
                        variant="outlined"
                        fullWidth
                        onClick={() => handleDepartmentClick(department, date)}
                        style={{ textAlign: 'left', textTransform: 'none', display: 'block' }}
                      >
                        <AttendanceCell
                          date={date}
                          department={department}
                          managerIds={managersList.map(manager => manager.staffId)}
                        />
                      </Button>
                    ))}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <div className="footer-content">
        <Button variant="outlined" onClick={() => setCurrentDate(dayjs())}>Today</Button>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DatePicker
            label={currentDate.format('MMMM YYYY')}
            value={currentDate}
            onChange={(newDate) => setCurrentDate(dayjs(newDate))}
          />
        </LocalizationProvider>
        <IconButton onClick={handlePrevWeek}>
          <ArrowBackIcon />
        </IconButton>
        <IconButton onClick={handleNextWeek}>
          <ArrowForwardIcon />
        </IconButton>
      </div>
    </div>
  );
};

export default HrCalendar;







