import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TableFooter,
  Paper, Button, IconButton, Box, Card, Typography, Checkbox, MenuItem, Select
} from '@mui/material';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import FilterListIcon from '@mui/icons-material/FilterList';
import '../../components/WeeklyCalendar/WeeklyCalendar.css'; // Ensure the correct path to your CSS file

import isSameOrAfter from 'dayjs/plugin/isSameOrAfter';
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore';

dayjs.extend(isSameOrAfter);
dayjs.extend(isSameOrBefore);


// Mock data
const mockEmployeeData = [
  {
    staff_id: 101,
    staff_fname: "Alice",
    staff_lname: "Smith",
    dept: "Sales",
    position: "Sales Manager",
    country: "USA",
    email: "alice.smith@company.com",
    reporting_manager: 201,
    role: 1
  },
  {
    staff_id: 102,
    staff_fname: "Bob",
    staff_lname: "Johnson",
    dept: "Engineering",
    position: "Software Engineer",
    country: "USA",
    email: "bob.johnson@company.com",
    reporting_manager: 202,
    role: 1
  }
];

const mockWFHScheduleData = [
  {
    request_id: 1,
    staff_id: 101,
    specific_date: "2024-10-14",
    is_am: true,
    is_pm: false,
    request_status: "approved"
  },
  {
    request_id: 2,
    staff_id: 102,
    specific_date: "2024-10-14",
    is_am: false,
    is_pm: true,
    request_status: "approved"
  },
  {
    request_id: 3,
    staff_id: 101,
    specific_date: "2024-10-15",
    is_am: true,
    is_pm: true,
    request_status: "approved"
  }
];



const HrCalendar = () => {
  const [currentDate, setCurrentDate] = useState(dayjs());
  const [scheduleData, setScheduleData] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [selectedEmployees, setSelectedEmployees] = useState([]);
  const [departmentFilterOpen, setDepartmentFilterOpen] = useState(false);
  const [availableEmployees, setAvailableEmployees] = useState([]);
  const navigate = useNavigate();

  const shifts = [
    { name: 'AM', time: '9:00 - 13:00' },
    { name: 'PM', time: '14:00 - 18:00' }
  ];

  useEffect(() => {
    const fetchScheduleData = () => {
        const weekStart = currentDate.startOf('week');
        const weekEnd = currentDate.endOf('week');

        // Loop through the week and get the department schedules for each day
        const weekDates = [];
        for (let date = weekStart; date.isSameOrBefore(weekEnd); date = date.add(1, 'day')) {
            const departmentSchedule = getDepartmentSchedule(date);
            weekDates.push({ date: date.format('YYYY-MM-DD'), departmentSchedule });
        }

        setScheduleData(weekDates);  // Store schedule for the entire week
    };

    fetchScheduleData();
}, [currentDate]);

const getDepartmentSchedule = (date) => {
  const departments = {};

  // Filter WFH schedule data by the selected department and specific date
  const filteredData = mockWFHScheduleData
    .filter(item => item.specific_date === date.format('YYYY-MM-DD'))
    .filter(item => {
      const employee = mockEmployeeData.find(emp => emp.staff_id === item.staff_id);
      return !selectedDepartment || (employee && employee.dept === selectedDepartment);
    });

  // Add WFH data into departments object
  filteredData.forEach((item) => {
      const employee = mockEmployeeData.find(emp => emp.staff_id === item.staff_id);
      if (employee && !departments[employee.dept]) {
        departments[employee.dept] = { office: 0, home: 0, total: 0 };
      }

      if (employee) {
        if (item.is_am || item.is_pm) {
          departments[employee.dept].home += 1;
        } else {
          departments[employee.dept].office += 1;
        }
        departments[employee.dept].total += 1;
      }
  });

  // Add default office days for employees without WFH records
  mockEmployeeData
    .filter(emp => !filteredData.some(item => item.staff_id === emp.staff_id))
    .filter(emp => !selectedDepartment || emp.dept === selectedDepartment)
    .forEach(emp => {
      if (!departments[emp.dept]) {
        departments[emp.dept] = { office: 0, home: 0, total: 0 };
      }
      departments[emp.dept].office += 1;  // Assume office
      departments[emp.dept].total += 1;
    });

  return departments;
};



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

  const handleFilterOpen = () => {
    setDepartmentFilterOpen(true);
  };

  const handleFilterClose = () => {
    setDepartmentFilterOpen(false);
  };

  const handleDepartmentChange = (event) => {
    const departmentName = event.target.value;
    setSelectedDepartment(departmentName);
  
    // Update available employees based on selected department using mockEmployeeData
    const employees = mockEmployeeData.filter(emp => emp.dept === departmentName);
    setAvailableEmployees(employees);
  };  

  const handleEmployeeSelection = (event) => {
    const { value } = event.target;
    setSelectedEmployees(typeof value === 'string' ? value.split(',') : value);
  };

  const handleDepartmentClick = (department, date) => {
    navigate('/hr/dept-view', { state: { department, date } });
  };

  return (
    <div className="weekly-schedule-container">
      {/* Filter Button */}
      <Button variant="outlined" onClick={handleFilterOpen} startIcon={<FilterListIcon />}>
        Filter
      </Button>

      {departmentFilterOpen && (
        <div className="filter-dropdown">
          <Box p={2} display="flex" flexDirection="column" gap={2}>
            {/* Department Filter */}
            <Select
              value={selectedDepartment}
              onChange={handleDepartmentChange}
              displayEmpty
              fullWidth
            >
              <MenuItem value=""><em>Select Department</em></MenuItem>
              {[...new Set(mockEmployeeData.map(emp => emp.dept))].map(dept => (
                <MenuItem key={dept} value={dept}>
                  {dept}
                </MenuItem>
              ))}
            </Select>


            {/* Employee Filter (Based on selected department) */}
            <Select
              multiple
              value={selectedEmployees}
              onChange={handleEmployeeSelection}
              displayEmpty
              fullWidth
            >
              <MenuItem disabled value="">
                <em>Select Employees</em>
              </MenuItem>
              {availableEmployees.map((emp) => (
                <MenuItem key={emp.staff_id} value={emp.staff_id}>
                  {`Employee ${emp.staff_id}`} {/* Use appropriate employee naming */}
                </MenuItem>
              ))}
            </Select>

            <Button variant="outlined" onClick={handleFilterClose}>
              Apply Filters
            </Button>
          </Box>
        </div>
      )}

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




