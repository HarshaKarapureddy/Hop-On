import React from 'react';
import { Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './Landing.css';
import './Auth.css';

export default function LandingPage() {
  const navigate = useNavigate();

return (
    <div className="landing-page">
        <Typography className="title" variant="h3" gutterBottom>
            Welcome to HopOn!
        </Typography>
        <Typography variant="h6" gutterBottom>
            Your journey to the best games starts here!
        </Typography>
        <div className="landing-button">
            <Button
                variant="contained"
                color="primary"
                onClick={() => navigate('/login')}
            >
                Login
            </Button>
            <Button
                variant="outlined"
                color="secondary"
                onClick={() => navigate('/signup')}
            >
                Sign Up
            </Button>
        </div>
    </div>
);
}
