import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from './pages/Home';
import Sidebar from './components/sidebar/sidebar';
import Navbar from './components/navbar/navbar';
import { useLocation } from 'react-router-dom';
import './App.css';  // Import the CSS file

function App() {
  return (
    <Router>
      <div className="app-layout">
        {/* <Navbar showDateSelector={showDateSelector} showSearch={showSearch} showProfile={showProfile} /> */}
        <Navbar />
        <Sidebar />  {/* Sidebar is included here, so it is rendered on every page */}
      </div>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
    </Router>
  );
}

export default App;