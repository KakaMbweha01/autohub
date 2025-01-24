import React from 'react'
import Header from './components/Header';
import Home from './pages/Home';
import Footer from './components/Footer';
import './assets/styles/global.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Favorites from './pages/Favorites';
import Notifications from './pages/Notifications';
import Search from './pages/Search';
import UserProfile from './pages/UserProfile';
import CarDetail from './components/CarDetails';
import CarList from './components/CarList';


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
          <Route path="/cardetail" element={<CarDetail />} />
          <Route path="/carlist" element={<CarList />} />
        </Routes>
      </Router>
      <Footer />
    </div>
  );
}

export default App;
