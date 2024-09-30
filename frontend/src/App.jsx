import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './pages/Home';
import Sidebar from './components/sidebar/sidebar';
import Navbar from './components/navbar/navbar';
import StaffViewSchedule from './pages/StaffViewSchedule';
import ManageerViewTeamSchedule from './pages/ManagerViewTeamSchedule';
import { useLocation } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-layout">
        <Navbar />
        <div className="main-container">
          <Sidebar />
          <div className="content-area">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/:staffId/Staff/Schedule" element={<StaffViewSchedule />} />
              <Route path="/:staffId/Manager/Schedule" element={<ManageerViewTeamSchedule />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;