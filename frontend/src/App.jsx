import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './pages/Home';
import StaffViewSchedule from './pages/StaffViewSchedule';
import Sidebar from './components/sidebar/sidebar';
import Navbar from './components/navbar/navbar';
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
              <Route path="/staff/view-schedule" element={<StaffViewSchedule />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;