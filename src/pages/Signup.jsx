import { useState } from 'react';
import { Button, TextField, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './Auth.css'; 

export default function Signup() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const navigate = useNavigate();
    // switch out for backend later
    const handleSignup = (e) => {
        e.preventDefault();
        if (password === confirmPassword) {
            alert('Signup Successful!');
            navigate('/login'); // Redirect to login page after successful signup
        } else {
            alert('Passwords do not match');
        }
    };

    return (
        <div className="auth-container">
            <Typography variant="h4" className="title" gutterBottom>
                Sign Up
                </Typography>
            <form onSubmit={handleSignup}>
                <TextField
                    label="Username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    fullWidth
                    className="input-field" 
                />
                <TextField
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    fullWidth
                    className="input-field"
                />
                <TextField
                    label="Confirm Password"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    fullWidth
                    margin="normal"
                    className="input-field"
                />
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Sign Up
                </Button>
            </form>
            <p> Already have an account? <a href="/login">Login here</a>.</p>
        </div>
    );
}
