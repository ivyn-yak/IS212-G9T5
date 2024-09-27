import React, { useState, useEffect } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TableFooter,
  Paper, Button, TextField, IconButton, InputAdornment, Box, Drawer, List, ListItem, ListItemText
} from '@mui/material';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import SearchIcon from '@mui/icons-material/Search';
import Card from '@mui/material/Card';
import './WeeklyCalendar.css';

// Mock data
const mockScheduleData = [
  { StaffID: '1', TeamID: 'A', Date: '2023-09-25', Work_from_home: true },
  { StaffID: '2', TeamID: 'A', Date: '2023-09-25', Work_from_home: false },
  { StaffID: '3', TeamID: 'A', Date: '2023-09-25', Work_from_home: true },
  { StaffID: '4', TeamID: 'A', Date: '2023-09-26', Work_from_home: false },
  { StaffID: '1', TeamID: 'A', Date: '2023-09-26', Work_from_home: false },
  { StaffID: '2', TeamID: 'A', Date: '2023-09-26', Work_from_home: false },
  { StaffID: '3', TeamID: 'A', Date: '2023-09-26', Work_from_home: true },
  { StaffID: '4', TeamID: 'A', Date: '2023-09-27', Work_from_home: true },
  { StaffID: '1', TeamID: 'A', Date: '2023-09-27', Work_from_home: true },
  { StaffID: '2', TeamID: 'A', Date: '2023-09-27', Work_from_home: false },
  { StaffID: '3', TeamID: 'A', Date: '2023-09-27', Work_from_home: false },
  { StaffID: '4', TeamID: 'A', Date: '2023-09-25', Work_from_home: false },
];

const mockStaffData = [
  { StaffID: '1', Name: 'John Doe' },
  { StaffID: '2', Name: 'Jane Smith' },
  { StaffID: '3', Name: 'Bob Johnson' },
  { StaffID: '4', Name: 'Alice Brown' },
];

const WeeklySchedule = () => {
  const [currentDate, setCurrentDate] = useState(dayjs());
  const [showSearch, setShowSearch] = useState(true);
  const [scheduleData, setScheduleData] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);

  const currentStaffID = '1'; // This would normally come from a cookie or auth context
  const currentTeamID = 'A'; // This would normally come from a cookie or auth context

  const shifts = [
    { name: 'AM', time: '9:00 - 13:00' },
    { name: 'PM', time: '14:00 - 18:00' }
  ];

  useEffect(() => {
    // Simulating database query
    const fetchScheduleData = () => {
      const weekStart = currentDate.startOf('week');
      const weekEnd = currentDate.endOf('week');
      
      const filteredData = mockScheduleData.filter(item => {
        const itemDate = dayjs(item.Date);
        return item.TeamID === currentTeamID && 
               itemDate.isAfter(weekStart) && 
               itemDate.isBefore(weekEnd);
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

  const getMySchedule = (date) => {
    const scheduleItem = scheduleData.find(item => 
      item.StaffID === currentStaffID && item.Date === date.format('YYYY-MM-DD')
    );
    return scheduleItem?.Work_from_home ? 'Home' : 'Office';
  };

  const getTeamSchedule = (date) => {
    const teamSchedule = scheduleData.filter(item => 
      item.Date === date.format('YYYY-MM-DD')
    );
    return teamSchedule.filter(item => !item.Work_from_home).length;
  };

  const handleTeamScheduleClick = (date) => {
    setSelectedDate(date);
    setSidebarOpen(true);
  };

  const renderSidebar = () => {
    if (!selectedDate) return null;

    const teamSchedule = scheduleData.filter(item => 
      item.Date === selectedDate.format('YYYY-MM-DD')
    );

    const inOffice = teamSchedule.filter(item => !item.Work_from_home);
    const atHome = teamSchedule.filter(item => item.Work_from_home);

    return (
      <Drawer anchor="right" open={sidebarOpen} onClose={() => setSidebarOpen(false)}>
        <Box sx={{ width: 250 }} role="presentation">
          <h2>Team Schedule for {selectedDate.format('MMM D, YYYY')}</h2>
          <h3>In Office:</h3>
          <List>
            {inOffice.map(item => (
              <ListItem key={item.StaffID}>
                <ListItemText primary={mockStaffData.find(staff => staff.StaffID === item.StaffID)?.Name} />
              </ListItem>
            ))}
          </List>
          <h3>Working from Home:</h3>
          <List>
            {atHome.map(item => (
              <ListItem key={item.StaffID}>
                <ListItemText primary={mockStaffData.find(staff => staff.StaffID === item.StaffID)?.Name} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
    );
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
                {weekDates.map((date) => (
                  <TableCell key={`${date.format('YYYY-MM-DD')}-${shift.name}`}>
                    <Card className="schedule-card">
                      <Box p={1}>
                        <b>My Schedule</b>
                        <br />
                        <span>Working From: {getMySchedule(date)}</span>
                      </Box>
                    </Card>
                    <Card className="schedule-card" onClick={() => handleTeamScheduleClick(date)}>
                      <Box p={1}>
                        <b>Team Schedule</b>
                        <br />
                        <span>Working from Office: {getTeamSchedule(date)}</span>
                      </Box>
                    </Card>
                  </TableCell>
                ))}
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
                      className="search-field"
                    />
                  )}

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
      {renderSidebar()}
    </div>
  );
};

export default WeeklySchedule;