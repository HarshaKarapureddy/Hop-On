import { Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import './Auth.css'
export default function Profile() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [userID, setUserID] = useState('');

    useEffect(() => {
        const storedUsername = localStorage.getItem('username');
        const storedPassword = localStorage.getItem('password');
        const storedUserID = localStorage.getItem('userID');
        setUsername(storedUsername || 'Not logged in');
        setPassword(storedPassword || 'Not logged in');
        setUserID(storedUserID || 'Not logged in');
    }, []);

    return (
        <div className="auth-container">
            <Typography className="title" variant="h4" gutterBottom>Profile Page</Typography>
            <Typography variant="h6">User Information:</Typography>
            <Typography variant="body1">Username: {username}</Typography>
            <Typography variant="body1">Password: {password}</Typography>
            <Typography variant="body1">User ID: {userID}</Typography>

            <Button
                variant="contained"
                color="primary"
                onClick={() => navigate('/homepage')}
                fullWidth
                style={{ marginTop: 16 }}
            >
                Go to Homepage
            </Button>
            <Button
                variant="contained"
                color="secondary"
                onClick={() => navigate('/search')}
                fullWidth
                style={{ marginTop: 8 }}
            >
                Go to Search
            </Button>
            <Button
                variant="contained"
                color="success"
                onClick={() => navigate('/review')}
                fullWidth
                style={{ marginTop: 8 }}
            >
                Go to Review
            </Button>
        </div>
    );
}
