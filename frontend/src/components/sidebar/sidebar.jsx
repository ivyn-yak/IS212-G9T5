import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Typography } from '@mui/material';
import { Home, ListAlt, ExitToApp, School } from '@mui/icons-material'; // Icons from Material-UI
import './sidebar.css';

const drawerWidth = 240;

const Sidebar = () => {
  return (
    <Drawer
      className="sideBar"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          backgroundColor: '#f4f4f4', // Sidebar background color
        },
      }}
      variant="permanent"
      anchor="left"
    >
      <div style={{ padding: '80px 30px 30px' }}>
        <Typography className="sidebar-heading">
          SCHEDULE
        </Typography>
        <List>
          {/* Schedule Section */}
          <ListItem button>
            <ListItemIcon>
              <ListAlt style={{ color: '#3f51b5' }} /> {/* Icon Color */}
            </ListItemIcon>
            <ListItemText primary="Schedule" />
          </ListItem>

          <Typography className="sidebar-heading">
            APPLICATION
          </Typography>

          {/* Application Section */}
          <ListItem button>
            <ListItemIcon>
              <Home style={{ color: '#3f51b5' }} />
            </ListItemIcon>
            <ListItemText primary="Requests" />
          </ListItem>

          <ListItem button>
            <ListItemIcon>
              <ListAlt style={{ color: '#3f51b5' }} />
            </ListItemIcon>
            <ListItemText primary="Apply" />
          </ListItem>

          <Typography className="sidebar-heading">
            WITHDRAWAL
          </Typography>

          {/* Withdrawal Section */}
          <ListItem button>
            <ListItemIcon>
              <School style={{ color: '#3f51b5' }} />
            </ListItemIcon>
            <ListItemText primary="Withdrawal" />
          </ListItem>

          <Typography className="sidebar-heading">
            OTHERS
          </Typography>

          {/* Others Section */}
          <ListItem button>
            <ListItemIcon>
              <ExitToApp style={{ color: '#3f51b5' }} />
            </ListItemIcon>
            <ListItemText primary="Logout" />
          </ListItem>
        </List>
      </div>
    </Drawer>
  );
};

export default Sidebar;

