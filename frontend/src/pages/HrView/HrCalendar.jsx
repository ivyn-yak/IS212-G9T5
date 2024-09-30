import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TableFooter,
  Paper, Button, IconButton, Box, Card
} from '@mui/material';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import '../../components/WeeklyCalendar/WeeklyCalendar.css'; // Ensure the correct path to your CSS file
import { Typography } from '@mui/material';



// Mock data
const mockScheduleData = [
  { StaffID: '1', Department: 'Sales', Date: '2024-09-25', Work_from_home: true },
  { StaffID: '2', Department: 'Sales', Date: '2024-09-25', Work_from_home: false },
  { StaffID: '3', Department: 'Marketing', Date: '2024-09-25', Work_from_home: true },
  { StaffID: '4', Department: 'Sales', Date: '2024-09-26', Work_from_home: false },
  { StaffID: '5', Department: 'Marketing', Date: '2024-09-26', Work_from_home: false },
  { StaffID: '6', Department: 'HR', Date: '2024-09-26', Work_from_home: false },
  { StaffID: '7', Department: 'HR', Date: '2024-09-26', Work_from_home: true },
  { StaffID: '8', Department: 'Sales', Date: '2024-09-27', Work_from_home: true },
  { StaffID: '9', Department: 'Sales', Date: '2024-09-27', Work_from_home: true },
  { StaffID: '10', Department: 'HR', Date: '2024-09-27', Work_from_home: false },
];

const HrCalendar = () => {
  const [currentDate, setCurrentDate] = useState(dayjs());
  const [scheduleData, setScheduleData] = useState([]);
  const navigate = useNavigate()

  const shifts = [
    { name: 'AM', time: '9:00 - 13:00' },
    { name: 'PM', time: '14:00 - 18:00' }
  ];

  useEffect(() => {
    // Simulate fetching schedule data for the current week
    const fetchScheduleData = () => {
      const weekStart = currentDate.startOf('week');
      const weekEnd = currentDate.endOf('week');

      const filteredData = mockScheduleData.filter(item => {
        const itemDate = dayjs(item.Date);
        return itemDate.isAfter(weekStart) && itemDate.isBefore(weekEnd);
      });

      setScheduleData(filteredData);
    };

    fetchScheduleData();
  }, [currentDate]);

  const getWeekDates = (date) => {
    const startOfWeek = date.startOf('week');
    return Array.from({ length: 7 }, (_, i) => startOfWeek.add(i, 'day'));
  };

  const weekDates = getWeekDates(currentDate);

  const handlePrevWeek = () => {
    setCurrentDate(currentDate.subtract(1, 'week'));
  };

  const handleNextWeek = () => {
    setCurrentDate(currentDate.add(1, 'week'));
  };

  const handleDateChange = (newDate) => {
    setCurrentDate(dayjs(newDate));
  };

  const handleDepartmentClick = (department, date) => {
    // Navigate to the TeamView component and pass department and date
    navigate('/hr/dept-view', { state: { department, date } });
  };

  const getDepartmentSchedule = (date) => {
    const departments = {};

    // Filter schedule data by date and calculate department stats
    scheduleData.filter(item => item.Date === date.format('YYYY-MM-DD')).forEach((item) => {
      if (!departments[item.Department]) {
        departments[item.Department] = { office: 0, home: 0, total: 0 };
      }
      if (item.Work_from_home) {
        departments[item.Department].home += 1;
      } else {
        departments[item.Department].office += 1;
      }
      departments[item.Department].total += 1; // Increment total count for the department
    });

    return departments;
  };

  return (
    <div className="weekly-schedule-container">
      <TableContainer component={Paper} className="centered-table-container">
        <Table className="styled-table">
          <TableHead>
            <TableRow>
              <TableCell>Shift</TableCell>
              {weekDates.map((date) => (
                <TableCell key={date.format('YYYY-MM-DD')}>
                  {date.format('ddd, MMM D')}
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
                {weekDates.map((date) => {
                  const departmentSchedule = getDepartmentSchedule(date);

                  return (
                    <TableCell key={`${date.format('YYYY-MM-DD')}-${shift.name}`}>
                      <Card className="schedule-card">
                        <Box p={1}>
                          {Object.entries(departmentSchedule).length > 0 ? (
                            Object.entries(departmentSchedule).map(([department, counts]) => (
                              <Box key={department} p={1}>
                                <Button 
                                  variant="outlined" 
                                  fullWidth
                                  onClick={() => handleDepartmentClick(department, date.format('YYYY-MM-DD'))}
                                  style={{ textAlign: 'left', textTransform: 'none', display: 'block' }}
                                >
                                  <Typography variant="body1" gutterBottom><strong>{department}</strong></Typography>
                                  <Typography variant="body2">Office: {counts.office}</Typography>
                                  <Typography variant="body2">Home: {counts.home}</Typography>
                                </Button>
                              </Box>

                            ))
                          ) : (
                            <Box>No departments scheduled</Box>
                          )}
                        </Box>
                      </Card>
                    </TableCell>
                  );
                })}
              </TableRow>
            ))}
          </TableBody>
          <TableFooter>
            <TableRow>
              <TableCell colSpan={8}>
                <div className="footer-content">
                  <Button variant="outlined" onClick={() => setCurrentDate(dayjs())}>
                    Today
                  </Button>

                  <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DatePicker 
                      label={currentDate.format('MMMM YYYY')}
                      value={currentDate}
                      onChange={handleDateChange}
                    />
                  </LocalizationProvider>

                  <IconButton onClick={handlePrevWeek}>
                    <ArrowBackIcon />
                  </IconButton>
                  <IconButton onClick={handleNextWeek}>
                    <ArrowForwardIcon />
                  </IconButton>
                </div>
              </TableCell>
            </TableRow>
          </TableFooter>
        </Table>
      </TableContainer>
    </div>
  );
};

export default HrCalendar;

