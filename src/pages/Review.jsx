import { useState } from 'react';
import { TextField, Button, Typography, Collapse, Alert, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import './Auth.css';
import './Search.css';
import axios from 'axios';

export default function Review() {
  const [userId, setUserId] = useState('');
  const [gameId, setGameId] = useState('');
  const [rating, setRating] = useState('');
  const [reviewText, setReviewText] = useState('');
  const [reviewId, setReviewId] = useState('');
  
  const [feedback, setFeedback] = useState({ message: '', type: '' });
  
  const [reviews, setReviews] = useState([]);

  const [showMake, setShowMake] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [showDelete, setShowDelete] = useState(false);
  const [showView, setShowView] = useState(false);

  const navigate = useNavigate();

  
  const API_BASE_URL = 'http://127.0.0.1:5000';
  
  const showFeedback = (message, type) => {
    setFeedback({ message, type });
    setTimeout(() => setFeedback({ message: '', type: '' }), 5000);
  };
  
  const resetFields = () => {
    setRating('');
    setReviewText('');
    setReviewId('');
  };

  const handleMakeReview = async (e) => {
    e.preventDefault();
    
    // Client-side validation
    if (!userId || !gameId || !rating || !reviewText) {
      showFeedback('Please fill in all fields.', 'error');
      return;
    }
    
    // Make sure userId is 6 digits
    if (!/^\d{6}$/.test(userId)) {
      showFeedback('User ID must be 6 digits.', 'error');
      return;
    }
    
    // Make sure gameId is a positive number
    if (!/^\d+$/.test(gameId) || parseInt(gameId) <= 0) {
      showFeedback('Game ID must be a positive number.', 'error');
      return;
    }
    
    // Make sure rating is between 1-5
    const ratingNum = parseInt(rating);
    if (isNaN(ratingNum) || ratingNum < 1 || ratingNum > 5) {
      showFeedback('Rating must be between 1 and 5.', 'error');
      return;
    }

    try { 
      console.log('Submitting review:', {
        user_id: userId,
        game_id: gameId,
        rating: ratingNum,
        review_text: reviewText
      });
      
      const response = await axios.post(`${API_BASE_URL}/reviews/make`, {
        user_id: userId,
        game_id: gameId,
        rating: ratingNum,
        review_text: reviewText
      });

      console.log('Review submission response:', response.data);
      
      if (response.data.status === 'error') {
        showFeedback(response.data.message || 'Failed to submit review.', 'error');
      } else {
        showFeedback('Review submitted successfully!', 'success');
        resetFields();
      }
    } catch (error) {
      console.error('Error submitting review:', error);
      console.error('Error response:', error.response?.data);
      showFeedback(
        error.response?.data?.message || 
        error.response?.data?.error || 
        'Failed to submit review. Please try again.', 
        'error'
      );
    }
  };

  const handleEditReview = async (e) => {
    e.preventDefault();
    
    // Client-side validation
    if (!reviewId || !rating || !reviewText) {
      showFeedback('Please fill in all fields.', 'error');
      return;
    }
    
    // Make sure reviewId is a positive number
    if (!/^\d+$/.test(reviewId) || parseInt(reviewId) <= 0) {
      showFeedback('Review ID must be a positive number.', 'error');
      return;
    }
    
    // Make sure rating is between 1-5
    const ratingNum = parseInt(rating);
    if (isNaN(ratingNum) || ratingNum < 1 || ratingNum > 5) {
      showFeedback('Rating must be between 1 and 5.', 'error');
      return;
    }
    
    try {
      console.log('Editing review:', {
        user_id: userId, 
        review_id: reviewId,
        new_rating: ratingNum,
        new_review_text: reviewText
      });
      
      const response = await axios.put(`${API_BASE_URL}/reviews/edit`, {
        user_id: userId, 
        review_id: reviewId,
        new_rating: ratingNum,
        new_review_text: reviewText
      });
      
      console.log('Review edited response:', response.data);
      
      if (response.data.status === 'error') {
        showFeedback(response.data.message || 'Failed to edit review.', 'error');
      } else {
        showFeedback('Review edited successfully!', 'success');
        resetFields();
      }
    } catch (error) {
      console.error('Error editing review:', error);
      console.error('Error response:', error.response?.data);
      showFeedback(
        error.response?.data?.message || 
        error.response?.data?.error || 
        'Failed to edit review. Please try again.', 
        'error'
      );
    }
  };

  const handleDeleteReview = async (e) => {
    e.preventDefault();
    
    // Client-side validation
    if (!userId || !reviewId) {
      showFeedback('Please fill in all fields.', 'error');
      return;
    }
    
    // Make sure userId is 6 digits
    if (!/^\d{6}$/.test(userId)) {
      showFeedback('User ID must be 6 digits.', 'error');
      return;
    }
    
    // Make sure reviewId is a positive number
    if (!/^\d+$/.test(reviewId) || parseInt(reviewId) <= 0) {
      showFeedback('Review ID must be a positive number.', 'error');
      return;
    }
    
    try {
      console.log('Deleting review:', {
        user_id: userId,
        review_id: reviewId
      });
      
      const response = await axios.delete(`${API_BASE_URL}/reviews/delete`, {
        data: {
          user_id: userId,
          review_id: reviewId
        }
      });
      
      console.log('Review deletion response:', response.data);
      
      if (response.data.status === 'error') {
        showFeedback(response.data.message || 'Failed to delete review.', 'error');
      } else {
        showFeedback('Review deleted successfully!', 'success');
        setUserId('');
        setGameId('');
        resetFields();
      }
    } catch (error) {
      console.error('Error deleting review:', error);
      console.error('Error response:', error.response?.data);
      showFeedback(
        error.response?.data?.message || 
        error.response?.data?.error || 
        'Failed to delete review. Please try again.', 
        'error'
      );
    }
  };

  const handleViewReviews = async (e) => {
    e.preventDefault();
    
    // Client-side validation
    if (!userId) {
      showFeedback('Please enter a User ID.', 'error');
      return;
    }
    
    // Make sure userId is 6 digits
    if (!/^\d{6}$/.test(userId)) {
      showFeedback('User ID must be 6 digits.', 'error');
      return;
    }
    
    try {
      console.log('Fetching reviews for user:', userId);
      const response = await axios.get(`${API_BASE_URL}/reviews/view`, {
        params: { user_id: userId }
      });
      
      console.log('Reviews response:', response.data);
      
      if (response.data.error || response.data.status === 'error') {
        showFeedback(
          response.data.message || 
          response.data.error || 
          'Failed to fetch reviews.', 
          'error'
        );
        setReviews([]);
      } else if (Array.isArray(response.data)) {
        setReviews(response.data);
        showFeedback(`Retrieved ${response.data.length} reviews`, 'success');
      } else {
        setReviews([]);
        showFeedback('No reviews found', 'info');
      }
    } catch (error) {
      console.error('Error fetching reviews:', error);
      console.error('Error response:', error.response?.data);
      showFeedback(
        error.response?.data?.message || 
        error.response?.data?.error || 
        'Failed to fetch reviews. Please try again.', 
        'error'
      );
    }
  };

  return (
    <div className="auth-container">
      <Typography variant="h4" className="title" gutterBottom>
        Review Page
      </Typography>

      {/* Feedback message */}
      {feedback.message && (
        <Alert 
          severity={feedback.type} 
          sx={{ width: '100%', marginBottom: 2 }}
          onClose={() => setFeedback({ message: '', type: '' })}
        >
          {feedback.message}
        </Alert>
      )}

      {/* Action buttons */}
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 20 }}>
        <Button variant="outlined" className="auth-button" onClick={() => setShowMake((prev) => !prev)}>Make a Review</Button>
        <Button variant="outlined" className="auth-button" onClick={() => setShowEdit((prev) => !prev)}>Edit a Review</Button>
        <Button variant="outlined" className="auth-button" onClick={() => setShowDelete((prev) => !prev)}>Delete a Review</Button>
        <Button variant="outlined" className="auth-button" onClick={() => setShowView((prev) => !prev)}>View All Reviews</Button>
      </div>

      {/* Make a Review */}
      <Collapse in={showMake}>
        <form onSubmit={handleMakeReview} style={{ marginBottom: 24, width: '100%' }}>
          <Typography variant="h6" className="title">Make a Review</Typography>
          <TextField
            label="User ID (6 digits)"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            required
            inputProps={{ maxLength: 6, pattern: "\\d{6}" }} 
            helperText="Located in your profile page"
          />
          <TextField
            label="Game ID"
            value={gameId}
            onChange={(e) => setGameId(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            required
            type="number"
            inputProps={{ min: 1 }}
            helperText="Find via the search page"
          />
          <TextField
            label="Rating (1-5)"
            type="number"
            value={rating}
            inputProps={{ min: 1, max: 5, step: 1 }}
            onChange={(e) => setRating(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            required
            helperText="Rate from 1 to 5"
          />
          <TextField
            label="Review Text"
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            fullWidth
            multiline
            rows={4}
            className="input-field"
            margin="normal"
            required
          />
          <Button 
            type="submit" 
            variant="contained" 
            color="primary" 
            fullWidth 
            className="auth-button"
            disabled={!userId || !gameId || !rating || !reviewText}
          >
            Submit Review
          </Button>
        </form>
      </Collapse>

      {/* Edit a Review */}
      <Collapse in={showEdit}>
        <form onSubmit={handleEditReview} style={{ marginBottom: 24, width: '100%' }}>
          <Typography variant="h6" className="title">Edit a Review</Typography>
          <TextField
            label="User ID (Optional)"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            inputProps={{ maxLength: 6, pattern: "\\d{6}" }}
            helperText="Must be exactly 6 digits"
          />
          <TextField
            label="Review ID"
            value={reviewId}
            onChange={(e) => setReviewId(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            required
            type="number"
            inputProps={{ min: 1 }}
            helperText="Must be a positive number"
          />
          <TextField
            label="New Rating (1-5)"
            type="number"
            value={rating}
            inputProps={{ min: 1, max: 5, step: 1 }}
            onChange={(e) => setRating(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            required
            helperText="Rate from 1 to 5"
          />
          <TextField
            label="New Review Text"
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            fullWidth
            multiline
            rows={4}
            className="input-field"
            margin="normal"
            required
          />
          <Button 
            type="submit" 
            variant="contained" 
            color="primary" 
            fullWidth 
            className="auth-button"
            disabled={!reviewId || !rating || !reviewText}
          >
            Edit Review
          </Button>
        </form>
      </Collapse>

      {/* Delete a Review */}
      <Collapse in={showDelete}>
        <form onSubmit={handleDeleteReview} style={{ marginBottom: 24, width: '100%' }}>
          <Typography variant="h6" className="title">Delete a Review</Typography>
          <TextField
            label="User ID (6 digits)"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            required
            inputProps={{ maxLength: 6, pattern: "\\d{6}" }}
            helperText="Must be exactly 6 digits"
          />
          <TextField
            label="Review ID"
            value={reviewId}
            onChange={(e) => setReviewId(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            required
            type="number"
            inputProps={{ min: 1 }}
            helperText="Must be a positive number"
          />
          <Button 
            type="submit" 
            variant="contained" 
            color="error" 
            fullWidth 
            className="auth-button"
            disabled={!userId || !reviewId}
          >
            Delete Review
          </Button>
        </form>
      </Collapse>

      {/* View Reviews */}
      <Collapse in={showView}>
        <form onSubmit={handleViewReviews} style={{ marginBottom: 24, width: '100%' }}>
          <Typography variant="h6" className="title">View All Reviews</Typography>
          <TextField
            label="User ID (6 digits)"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            fullWidth
            className="input-field"
            margin="normal"
            required
            inputProps={{ maxLength: 6, pattern: "\\d{6}" }}
            helperText="Must be exactly 6 digits"
          />
          <Button 
            type="submit" 
            variant="outlined" 
            fullWidth 
            className="auth-button"
            disabled={!userId}
          >
            View Reviews
          </Button>
        </form>
        
        {/* Display retrieved reviews */}
        {reviews.length > 0 && (
      <div style={{ width: '100%', marginTop: 20 }}>
        <div className="results-container" style={{ marginBottom: 20 }}>
          <div className="results-list">
            {reviews.map((review, index) => (
              <div key={index} className="result-item">
                <Paper 
                  elevation={1} 
                  sx={{ padding: 2, marginBottom: 2, backgroundColor: '#f9f9f9' }}
                >
                  <Typography variant="body1"><strong>Review ID:</strong> {review[0]}</Typography>
                  <Typography variant="body1"><strong>User ID:</strong> {review[1]}</Typography>
                  <Typography variant="body1"><strong>Game ID:</strong> {review[2]}</Typography>
                  <Typography variant="body1"><strong>Game Name:</strong> {review[3]}</Typography>
                  <Typography variant="body1"><strong>Genre:</strong> {review[4]}</Typography>
                  <Typography variant="body1"><strong>Rating:</strong> {review[5]}/5</Typography>
                  <Typography variant="body1"><strong>Review:</strong> {review[6]}</Typography>
                </Paper>
              </div>
            ))}
          </div>
      </div>
    </div>
)}
      </Collapse>

      {/* Navigation buttons */}
      <div style={{ marginTop: 30, width: '100%' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/homepage')}
          fullWidth
          className="auth-button"
          style={{ marginBottom: 8 }}
        >
          Go to Homepage
        </Button>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => navigate('/search')}
          fullWidth
          className="auth-button"
          style={{ marginBottom: 8 }}
        >
          Go to Search
        </Button>
        <Button
          variant="contained"
          color="success"
          onClick={() => navigate('/profile')}
          fullWidth
          className="auth-button"
        >
          Go to Profile
        </Button>
      </div>
    </div>
  );
}