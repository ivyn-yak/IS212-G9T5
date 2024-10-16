import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './pages/Home';
import StaffViewSchedule from './pages/StaffViewSchedule';
import DeptView from './pages/HrView/DeptView';
import HrCalendar from './pages/HrView/HrCalendar';
import Sidebar from './components/sidebar/sidebar';
import Navbar from './components/navbar/navbar';
import ManageerViewTeamSchedule from './pages/ManagerViewTeamSchedule';
import WithdrawalFormView from './pages/WithdrawalFormView';
import { useLocation } from 'react-router-dom';
import './App.css';
import StaffRequestsView from './pages/StaffRequestsView';

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
              <Route path="/hr/dept-view" element={<DeptView />} />
              <Route path="/hr/hr-calendar" element={<HrCalendar />} />
              <Route path="/:staffId/Staff/Schedule" element={<StaffViewSchedule />} />
              <Route path="/:staffId/Manager/Schedule" element={<ManageerViewTeamSchedule />} />
              <Route path="/:staffId/Staff/Application/Requests" element={<StaffRequestsView />} />
              <Route path="/:staffId/Staff/Withdrawal" element={<WithdrawalFormView />} />
              <Route path="*" element={<div>404 Not Found</div>} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;