import { Button, Typography, List, ListItem } from '@mui/material';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Homepage.css';  
import './Auth.css';
export default function Homepage() {
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState([]);

  const handleRecommendationClick = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/recommendations', {
        userID: '123456', // Static user ID for now
      });

      if (response.data.recommendations) {
        setRecommendations(response.data.recommendations);
      } else {
        console.log("No recommendations found.");
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  return (
    <div className="auth-container">
      <Typography className="title" variant="h4" gutterBottom>Homepage</Typography>

      {/* Styled Navigation Buttons */}
      <div style={{ marginTop: 40, width: '100%' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate("/profile")}
          fullWidth
          className="auth-button"
        >
          Go to Profile
        </Button>

        <Button
          variant="contained"
          color="secondary"
          onClick={() => navigate("/search")}
          fullWidth
          className="auth-button"
        >
          Go to Search
        </Button>

        <Button
          variant="contained"
          color="success"
          onClick={() => navigate("/review")}
          fullWidth
          className="auth-button"
        >
          Go to Review
        </Button>

        <Button
          variant="contained"
          color="error"
          onClick={() => navigate("/")}
          fullWidth
        >
          Log Out
        </Button>
      
        <Typography className="recommendation-prompt" variant="h5" gutterBottom style={{ marginTop: 40 }}>
          Want to find your next favorite Game? Click Here!
        </Typography>

        {/* Button to fetch recommendations */}
        <Button
          variant="contained"
          onClick={handleRecommendationClick}
          fullWidth
          className="reccomendation-button"
          style={{ marginTop: 10, backgroundColor: 'tan' }}
        >
          Get Game Recommendations
        </Button>

        {/* Display Recommendations */}
        {recommendations.length > 0 && (
          <div className="results-container">
            <Typography variant="h6">Recommendations:</Typography>
            <List className="results-list">
              {recommendations.map((game, index) => (
                <ListItem key={index} className="result-item">
                  <Typography variant="subtitle1"><strong>{game.name}</strong></Typography>
                  <Typography variant="body2">{game.release_year}</Typography>
                  <Typography variant="body2">{game.genres.join(", ")}</Typography>
                </ListItem>
              ))}
            </List>
          </div>
        )}
      </div>
    </div>
  );
}
