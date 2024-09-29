import React, { useState, useEffect } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TableFooter,
  Paper, Button, TextField, IconButton, InputAdornment, Box, Drawer, List, ListItem, ListItemText,
  Typography
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
const mockScheduleData = {
  staff: {
    staffID: '1',
    scheduleTrails: [
      { date: '2023-09-25', is_am: true, is_pm: true },
      { date: '2023-09-26', is_am: false, is_pm: true },
      { date: '2023-09-27', is_am: true, is_pm: false },
    ]
  },
  team: [
    {
      staffID: '1',
      name: 'John Doe',
      scheduleTrails: [
        { date: '2023-09-25', is_am: true, is_pm: true },
        { date: '2023-09-26', is_am: false, is_pm: true },
        { date: '2023-09-27', is_am: true, is_pm: false },
      ]
    },
    {
      staffID: '2',
      name: 'Jane Smith',
      scheduleTrails: [
        { date: '2023-09-25', is_am: false, is_pm: false },
        { date: '2023-09-26', is_am: true, is_pm: true },
      ]
    },
    {
      staffID: '3',
      name: 'Bob Johnson',
      scheduleTrails: [
        { date: '2023-09-27', is_am: true, is_pm: true },
      ]
    },
  ]
};

const WeeklySchedule = () => {
  const [currentDate, setCurrentDate] = useState(dayjs());
  const [showSearch, setShowSearch] = useState(true);
  const [scheduleData, setScheduleData] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedShift, setSelectedShift] = useState(null);

  const shifts = [
    { name: 'AM', time: '9:00 - 13:00' },
    { name: 'PM', time: '14:00 - 18:00' }
  ];

  useEffect(() => {
    // Simulating API call to fetch schedule data
    const fetchScheduleData = () => {
      // In a real application, you would make an API call here
      // For now, we'll just use the mock data
      setScheduleData(mockScheduleData);
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

  const getMySchedule = (date, shift) => {
    if (!scheduleData) return 'Office'; // Default to office if data isn't loaded

    const dateString = date.format('YYYY-MM-DD');
    const scheduleItem = scheduleData.staff.scheduleTrails.find(item => item.date === dateString);
    
    if (!scheduleItem) return 'Office'; // Default to office if no schedule found for this date
    
    if (shift === 'AM' && scheduleItem.is_am) return 'Home';
    if (shift === 'PM' && scheduleItem.is_pm) return 'Home';
    
    return 'Office';
  };

  const getTeamSchedule = (date, shift) => {
    if (!scheduleData) return 0;

    const dateString = date.format('YYYY-MM-DD');
    return scheduleData.team.filter(member => {
      const scheduleItem = member.scheduleTrails.find(item => item.date === dateString);
      if (!scheduleItem) return true; // Count as in office if no schedule found
      return shift === 'AM' ? !scheduleItem.is_am : !scheduleItem.is_pm;
    }).length;
  };

  const handleTeamScheduleClick = (date, shift) => {
    setSelectedDate(date);
    setSelectedShift(shift.name);
    setSidebarOpen(true);
  };

  const renderSidebar = () => {
    if (!selectedDate || !selectedShift || !scheduleData) return null;

    const dateString = selectedDate.format('YYYY-MM-DD');
    const isAM = selectedShift === 'AM';

    const inOffice = scheduleData.team.filter(member => {
      const scheduleItem = member.scheduleTrails.find(item => item.date === dateString);
      if (!scheduleItem) return true; // Count as in office if no schedule found
      return isAM ? !scheduleItem.is_am : !scheduleItem.is_pm;
    });

    const atHome = scheduleData.team.filter(member => {
      const scheduleItem = member.scheduleTrails.find(item => item.date === dateString);
      if (!scheduleItem) return false; // Don't count as at home if no schedule found
      return isAM ? scheduleItem.is_am : scheduleItem.is_pm;
    });

    return (
      <Drawer anchor="right" open={sidebarOpen} onClose={() => setSidebarOpen(false)}>
        <Box className="sidebar-content" role="presentation">
          <Typography variant="h4" className="sidebar-title">
            Team Schedule
          </Typography>
          <Typography variant="h5" className="sidebar-date">
            {selectedDate.format('MMM D, YYYY')}
          </Typography>
          <Typography variant="subtitle1" className="sidebar-shift">
            {selectedShift}
          </Typography>
          <Typography variant="h6" className="sidebar-subtitle">In Office:</Typography>
          <List>
            {inOffice.map(member => (
              <ListItem key={member.staffID}>
                <ListItemText primary={member.name} />
              </ListItem>
            ))}
          </List>
          <Typography variant="h6" className="sidebar-subtitle">Working from Home:</Typography>
          <List>
            {atHome.map(member => (
              <ListItem key={member.staffID}>
                <ListItemText primary={member.name} />
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
                        <span>Working From: {getMySchedule(date, shift.name)}</span>
                      </Box>
                    </Card>
                    <Card className="schedule-card" onClick={() => handleTeamScheduleClick(date, shift)}>
                      <Box p={1}>
                        <b>Team Schedule</b>
                        <br />
                        <span>Working from Office: {getTeamSchedule(date, shift.name)}</span>
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