import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
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

// Mock API function
const fetchScheduleData = async (staffId, startDate, endDate) => {
  try {
    const response = await fetch(`/api/staff/${staffId}/wfh_office_dates?start_date=${startDate}&end_date=${endDate}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Transform the data to match the structure expected by the component
    return {
      staff: {
        staffID: data.staff.staff_id,
        scheduleTrails: data.staff.ScheduleDetails.map(detail => ({
          date: detail.specific_date,
          is_am: detail.is_am,
          is_pm: detail.is_pm
        }))
      },
      team: data.team.map(member => ({
        staffID: member.staff_id.toString(),
        scheduleTrails: member.ScheduleDetails.map(detail => ({
          date: detail.specific_date,
          is_am: detail.is_am,
          is_pm: detail.is_pm
        }))
      }))
    };
  } catch (error) {
    console.error('Error fetching schedule data:', error);
    throw error;
  }
};

const WeeklySchedule = () => {
  const { staffId } = useParams();
  const [selectedWeekStart, setSelectedWeekStart] = useState(dayjs().startOf('week'));
  const [scheduleData, setScheduleData] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedShift, setSelectedShift] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [highlightedStaffId, setHighlightedStaffId] = useState(null);

  const shifts = [
    { name: 'AM', time: '9:00 - 13:00' },
    { name: 'PM', time: '14:00 - 18:00' }
  ];
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const startOfWeek = selectedWeekStart.format('YYYY-MM-DD');
        const endOfWeek = selectedWeekStart.endOf('week').format('YYYY-MM-DD');
        const data = await fetchScheduleData(staffId, startOfWeek, endOfWeek);
        console.log('Fetched schedule data:', data);
        setScheduleData(data);
      } catch (error) {
        console.error('Error fetching schedule data:', error);
        // You might want to set an error state here and display it to the user
      }
    };
  
    fetchData();
  }, [staffId, selectedWeekStart]);

  const getWeekDates = (date) => {
    return Array.from({ length: 7 }, (_, i) => date.add(i, 'day'));
  };

  const weekDates = getWeekDates(selectedWeekStart);

  const handlePrevWeek = () => {
    setSelectedWeekStart(selectedWeekStart.subtract(1, 'week'));
  };

  const handleNextWeek = () => {
    setSelectedWeekStart(selectedWeekStart.add(1, 'week'));
  };

  const handleDateChange = (newDate) => {
    setSelectedWeekStart(dayjs(newDate).startOf('week'));
  };

  const handleTodayClick = () => {
    setSelectedWeekStart(dayjs().startOf('week'));
  };

  const getMySchedule = (date, shift) => {
    console.log(`Getting schedule for date: ${date.format('YYYY-MM-DD')}, shift: ${shift}`);
    if (!scheduleData) {
      console.log('Schedule data not loaded yet');
      return 'Office'; // Default to office if data isn't loaded
    }

    const dateString = date.format('YYYY-MM-DD');
    console.log('Looking for schedule item with date:', dateString);
    console.log('Available schedule trails:', scheduleData.staff.scheduleTrails);

    const scheduleItem = scheduleData.staff.scheduleTrails.find(item => item.date === dateString);
    
    console.log('Schedule item found:', scheduleItem);

    if (!scheduleItem) {
      console.log('No schedule item found for this date, defaulting to Office');
      return 'Office'; // Default to office if no schedule found for this date
    }
    
    if (shift === 'AM' && scheduleItem.is_am) {
      console.log('AM shift and is_am is true, returning Home');
      return 'Home';
    }
    if (shift === 'PM' && scheduleItem.is_pm) {
      console.log('PM shift and is_pm is true, returning Home');
      return 'Home';
    }
    
    console.log('Defaulting to Office');
    return 'Office';
  };

  const handleSearchChange = (event) => {
    const newSearchTerm = event.target.value;
    setSearchTerm(newSearchTerm);
    
    if (newSearchTerm.trim() === '') {
      setHighlightedStaffId(null);  // Clear highlight when search is empty
    } else {
      const foundStaff = scheduleData?.team.find(
        staff => staff.name.toLowerCase().includes(newSearchTerm.toLowerCase())
      );
      setHighlightedStaffId(foundStaff ? foundStaff.staffID : null);
    }
  };

  const getTeamSchedule = (date, shift) => {
    if (!scheduleData) return { inOffice: 0, atHome: 0 };

    const dateString = date.format('YYYY-MM-DD');
    const inOffice = scheduleData.team.filter(member => {
      const scheduleItem = member.scheduleTrails.find(item => item.date === dateString);
      if (!scheduleItem) return true; // Count as in office if no schedule found
      return shift === 'AM' ? !scheduleItem.is_am : !scheduleItem.is_pm;
    });
    const atHome = scheduleData.team.filter(member => {
      const scheduleItem = member.scheduleTrails.find(item => item.date === dateString);
      if (!scheduleItem) return false; // Don't count as at home if no schedule found
      return shift === 'AM' ? scheduleItem.is_am : scheduleItem.is_pm;
    });
    return { inOffice: inOffice.length, atHome: atHome.length };
  };

  const isHighlightedStaffAtHome = (date, shift) => {
    if (!highlightedStaffId || !scheduleData) return false;
    const staff = scheduleData.team.find(s => s.staffID === highlightedStaffId);
    if (!staff) return false;
    const dateString = date.format('YYYY-MM-DD');
    const scheduleItem = staff.scheduleTrails.find(item => item.date === dateString);
    if (!scheduleItem) return false;
    return shift === 'AM' ? scheduleItem.is_am : scheduleItem.is_pm;
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
              <ListItem key={member.staffID} style={{ backgroundColor: member.staffID === highlightedStaffId ? '#e8f5e9' : 'transparent' }}>
                <ListItemText primary={member.name} />
              </ListItem>
            ))}
          </List>
          <Typography variant="h6" className="sidebar-subtitle">Working from Home:</Typography>
          <List>
            {atHome.map(member => (
              <ListItem key={member.staffID} style={{ backgroundColor: member.staffID === highlightedStaffId ? '#e8f5e9' : 'transparent' }}>
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
                {weekDates.map((date) => {
                  const { inOffice, atHome } = getTeamSchedule(date, shift.name);
                  const isHighlighted = highlightedStaffId && isHighlightedStaffAtHome(date, shift.name);                  return (
                    <TableCell key={`${date.format('YYYY-MM-DD')}-${shift.name}`}>
                      <Card className="schedule-card">
                        <Box p={1}>
                          <b>My Schedule</b>
                          <br />
                          <span>Working From: {getMySchedule(date, shift.name)}</span>
                        </Box>
                      </Card>
                      <Card 
                         className={`schedule-card team-schedule-card ${isHighlighted ? 'highlighted' : ''}`} 
                        onClick={() => handleTeamScheduleClick(date, shift)}
                        style={{ backgroundColor: isHighlighted ? '#e8f5e9' : 'transparent' }}
                      >
                        <Box p={1}>
                          <b>Team Schedule</b>
                          <br />
                          <span>Working from Office: {inOffice}</span>
                          <br />
                          <span>Working from Home: {atHome}</span> <br />
                          <Typography 
                            variant="caption" 
                            className="highlight-text"
                            style={{ 
                              color: 'green', 
                              visibility: isHighlighted ? 'visible' : 'hidden',
                              height: '1.2em',  // Reduced height
                              marginTop: '2px'
                            }}
                          >
                            Highlighted staff Working from Home
                          </Typography>
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
                  <Button variant="outlined" onClick={handleTodayClick}>
                    Today
                  </Button>
                  <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DatePicker 
                      label={selectedWeekStart.format('MMMM YYYY')}
                      value={selectedWeekStart}
                      onChange={handleDateChange}
                    />
                  </LocalizationProvider>
                  <TextField
                    variant="outlined"
                    placeholder="Search staff..."
                    value={searchTerm}
                    onChange={handleSearchChange}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <SearchIcon />
                        </InputAdornment>
                      ),
                    }}
                    className="search-field"
                  />
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