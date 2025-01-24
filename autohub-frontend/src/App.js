import React from 'react'
import Header from './components/Header';
import Home from './pages/Home';
import './assets/styles/global.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Favorites from './pages/Favorites';
import Notifications from './pages/Notifications';
import Search from './pages/Search';
import UserProfile from './pages/UserProfile';


function App() {
  return (
    <div>
      <Header />
      <Home />
      <Router>
        <Routes>
          <Route path="/favorites" element={<Favorites />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/search" element={<Search />} />
          <Route path="/profile" element={<UserProfile />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
