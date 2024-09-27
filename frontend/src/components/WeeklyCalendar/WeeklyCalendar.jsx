import React, { useState } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TableFooter,
  Paper, Button, TextField, IconButton, InputAdornment, Box
} from '@mui/material';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import SearchIcon from '@mui/icons-material/Search';
import './WeeklyCalendar.css';

const WeeklySchedule = () => {
  const [currentDate, setCurrentDate] = useState(dayjs());
  const [showSearch, setShowSearch] = useState(true);

  const shifts = [
    { name: 'AM', time: '9:00 - 13:00' },
    { name: 'PM', time: '14:00 - 18:00' }
  ];

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
                    {/* You can add your schedule items here */}
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
    </div>
  );
};

export default WeeklySchedule;