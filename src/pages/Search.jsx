import { useState } from 'react';
import { TextField, Button, Typography, List, ListItem } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './Auth.css';
import './search.css';

export default function Search() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [error, setError] = useState(''); // To show error if there's any issue
    const navigate = useNavigate();

    const handleSearch = async (e) => {
        e.preventDefault();
        setError('');  // Clear any previous error

        try {
            // Update the URL
            const response = await fetch(`http://localhost:5000/api/search?q=${encodeURIComponent(query)}`);
            
            if (!response.ok) {
                throw new Error('Search failed');
            }

            const data = await response.json();

            // Check for errors
            if (data.error) {
                setError(data.error);
                setResults([]);
            } else {
                setResults(data); // results in array
            }
        } catch (err) {
            setError('An error occurred while searching.');
            console.error('Search failed:', err);
        }
    };

    return (
        <div className="auth-container">
            <Typography variant="h4" className="title" gutterBottom>
                Search Page
            </Typography>
            <form onSubmit={handleSearch}>
                <TextField
                    label="Search Games"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    fullWidth
                    className="input-field"
                />
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Search
                </Button>
            </form>

            {/* Error Display */}
            {error && <Typography variant="body1" color="error" style={{ marginTop: 20 }}>{error}</Typography>}

            {/* Display Results */}
            {results.length > 0 && (
                <div className="results-container">
                <Typography variant="h6">Results:</Typography>
                <List className="results-list">
                    {results.map((result, index) => (
                        <ListItem key={index} className="result-item">
                            <Typography variant="subtitle1"><strong>{result.name}</strong></Typography>
                            <Typography variant="body2">ID: {result.id}</Typography>
                            
                        </ListItem>
                    ))}
                </List>
            </div>
            )}

            <div style={{ marginTop: 40 }}>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => navigate('/homepage')}
                    fullWidth
                    style={{ marginBottom: 8 }}
                >
                    Go to Homepage
                </Button>
                <Button
                    variant="contained"
                    color="secondary"
                    onClick={() => navigate('/profile')}
                    fullWidth
                >
                    Go to Profile
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
        </div>
    );
}
