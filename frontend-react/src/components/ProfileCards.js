import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  IconButton,
  CircularProgress,
  Button,
  Alert,
} from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';
import CloseIcon from '@mui/icons-material/Close';
import { getNextProfile, recordSwipe } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function ProfileCards() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();
  const [currentProfile, setCurrentProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionInProgress, setActionInProgress] = useState(false);

  const fetchNextProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      const profile = await getNextProfile();
      setCurrentProfile(profile);
    } catch (error) {
      console.error('Error fetching profile:', error);
      if (error.message.includes('No more profiles available')) {
        setCurrentProfile(null);
      } else {
        setError(error.message);
        if (error.message.includes('Unauthorized')) {
          logout();
          navigate('/login');
        }
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchNextProfile();
    } else {
      navigate('/login');
    }
  }, [token, navigate]);

  const handleSwipe = async (liked) => {
    if (actionInProgress || !currentProfile) return;

    try {
      setActionInProgress(true);
      await recordSwipe(currentProfile._id, liked);
      await fetchNextProfile();
    } catch (error) {
      console.error('Error recording swipe:', error);
      setError(error.message);
    } finally {
      setActionInProgress(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" flexDirection="column" alignItems="center" gap={2} p={3}>
        <Alert severity="error">{error}</Alert>
        <Button variant="contained" onClick={fetchNextProfile}>
          Try Again
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
        <Button variant="outlined" color="primary" onClick={logout}>
          Logout
        </Button>
      </Box>

      {!currentProfile ? (
        <Card sx={{ height: '70vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Box sx={{ textAlign: 'center', p: 3 }}>
            <Typography variant="h5" color="text.secondary" gutterBottom>
              No more profiles to show!
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Check back later for more matches
            </Typography>
          </Box>
        </Card>
      ) : (
        <>
          <Card sx={{ position: 'relative', mb: 2 }}>
            <CardMedia
              component="img"
              height="400"
              image={currentProfile.profile_image || 'https://via.placeholder.com/400x400'}
              alt={currentProfile.name}
            />
            <CardContent>
              <Typography variant="h4" component="div">
                {currentProfile.name}, {currentProfile.age}
              </Typography>
              <Typography variant="body1" color="text.secondary" gutterBottom>
                {currentProfile.location || 'Unknown location'}
              </Typography>
              {currentProfile.profession && (
                <Typography variant="body1" color="text.secondary">
                  {currentProfile.profession}
                </Typography>
              )}
            </CardContent>
          </Card>

          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 4, my: 2 }}>
            <IconButton
              onClick={() => handleSwipe(false)}
              disabled={actionInProgress}
              sx={{
                backgroundColor: '#ff4444',
                color: 'white',
                '&:hover': { backgroundColor: '#cc0000' },
                '&.Mui-disabled': { backgroundColor: '#ffcccc' },
                width: 64,
                height: 64,
              }}
            >
              <CloseIcon fontSize="large" />
            </IconButton>
            <IconButton
              onClick={() => handleSwipe(true)}
              disabled={actionInProgress}
              sx={{
                backgroundColor: '#00C851',
                color: 'white',
                '&:hover': { backgroundColor: '#007E33' },
                '&.Mui-disabled': { backgroundColor: '#ccffcc' },
                width: 64,
                height: 64,
              }}
            >
              <FavoriteIcon fontSize="large" />
            </IconButton>
          </Box>
        </>
      )}
    </Box>
  );
}

export default ProfileCards; 