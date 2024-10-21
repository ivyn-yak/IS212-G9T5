import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Typography } from '@mui/material';
import { Home, ListAlt, ExitToApp, School, CalendarToday, Assignment } from '@mui/icons-material';
import './sidebar.css';

const Sidebar = () => {
  const { staffId } = useParams();

  return (
    <Drawer
      className="sideBar"
      variant="permanent"
      anchor="left"
    >
      <div className="sidebar-content">
        <Typography className="sidebar-heading">
          SCHEDULE
        </Typography>
        <List>
          <ListItem button component={Link} to={`/${staffId}/`}>
            <ListItemIcon>
              <Home className="sidebar-icon" />
            </ListItemIcon>
            <ListItemText primary="Home" />
          </ListItem>
          <ListItem button component={Link} to={`/${staffId}/Staff/Schedule`}>
            <ListItemIcon>
              <CalendarToday className="sidebar-icon" />
            </ListItemIcon>
            <ListItemText primary="Schedule" />
          </ListItem>

          <Typography className="sidebar-heading">
            APPLICATION
          </Typography>

          <ListItem button component={Link} to={`/${staffId}/Staff/Application/Requests`}>
            <ListItemIcon>
              <Assignment className="sidebar-icon" />
            </ListItemIcon>
            <ListItemText primary="Requests" />
          </ListItem>

          <ListItem button component={Link} to={`/${staffId}/Staff/WFHRequestForm`}>
            <ListItemIcon>
              <ListAlt className="sidebar-icon" />
            </ListItemIcon>
            <ListItemText primary="Apply" />
          </ListItem>

          <Typography className="sidebar-heading">
            WITHDRAWAL
          </Typography>

          <ListItem button component={Link} to={`/${staffId}/Staff/Withdrawal`}>
            <ListItemIcon>
              <School className="sidebar-icon" />
            </ListItemIcon>
            <ListItemText primary="Withdrawal" />
          </ListItem>

          <Typography className="sidebar-heading">
            OTHERS
          </Typography>

          <ListItem button component={Link} to="/logout">
            <ListItemIcon>
              <ExitToApp className="sidebar-icon" />
            </ListItemIcon>
            <ListItemText primary="Logout" />
          </ListItem>
        </List>
      </div>
    </Drawer>
  );
};

export default Sidebar;