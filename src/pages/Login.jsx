import { useState } from 'react';
import { Button, TextField, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './Auth.css'; 

export default function Login({ setIsLoggedIn }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [UserID, setUserID] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();
        // mock login 
        if (username === 'testuser' && password === 'password') {
            setIsLoggedIn(true); // Set logged-in state to true
            localStorage.setItem('username', username);
            localStorage.setItem('password', password);
            localStorage.setItem('userID', '123456');
            navigate('/homepage'); // Redirect to homepage
        } else {
            alert('Invalid login');
        }
    };

    return (
        <div className="auth-container">
            <Typography variant="h4" className="title" gutterBottom>
                Login
                </Typography>
            <form onSubmit={handleLogin}>
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
                <Button type="submit" variant="contained" color="primary" className="login-button" fullWidth>
                    Login
                </Button>
            </form>
            <p>Don't have an account? <a href="/signup">Sign Up here</a>.</p>
        </div>
    );
}
