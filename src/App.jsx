import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import LandingPage from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Homepage from './pages/Homepage';
import Profile from './pages/Profile';
import Search from './pages/Search';
import { Navigate } from 'react-router-dom';
import Review from './pages/Review';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/signup" element={<Signup />} />

        <Route
          path="/homepage"
          element={isLoggedIn ? <Homepage /> : <Navigate to="/login" />}
        />
        <Route
          path="/profile"
          element={isLoggedIn ? <Profile /> : <Navigate to="/login" />}
        />
        <Route
          path="/search"
          element={isLoggedIn ? <Search /> : <Navigate to="/login" />}
        />
        <Route
          path="/review"
          element={isLoggedIn ? <Review /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
