import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  TextField,
  Button,
  CircularProgress,
  Avatar,
  CardMedia,
  CardActions,
  Chip,
  Stack,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import WorkIcon from '@mui/icons-material/Work';
import SchoolIcon from '@mui/icons-material/School';
import { getRecommendations } from '../services/api';

function RecommendationList() {
  const [searchQuery, setSearchQuery] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = async (search = '') => {
    try {
      setLoading(true);
      const response = await getRecommendations();
      setMessage(response.message || '');
      setRecommendations(response.profiles || []);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setMessage('Error loading recommendations');
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleSearch = () => {
    fetchRecommendations(searchQuery);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <Box sx={{ p: 3, backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      {/* Search section */}
      <Box sx={{ mb: 4, display: 'flex', gap: 2 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Search by location..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          sx={{ bgcolor: 'white' }}
        />
        <Button
          variant="contained"
          startIcon={<SearchIcon />}
          onClick={handleSearch}
          sx={{ px: 4 }}
        >
          Search
        </Button>
      </Box>

      {/* Loading indicator */}
      {loading && (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      )}

      {/* Message display */}
      {!loading && message && (
        <Box textAlign="center" mb={4}>
          <Typography 
            variant="h6" 
            color={recommendations.length > 0 ? "primary" : "text.secondary"}
            gutterBottom
          >
            {message}
          </Typography>
        </Box>
      )}

      {/* Recommendations grid */}
      {recommendations.length > 0 && (
        <Grid container spacing={3}>
          {recommendations.map((profile) => (
            <Grid item xs={12} sm={6} md={4} key={profile._id}>
              <Card elevation={3} sx={{ height: '100%', ':hover': { boxShadow: 6 } }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={profile.profile_image || 'https://via.placeholder.com/200'}
                  alt={profile.name}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {profile.name}, {profile.age}
                  </Typography>
                  
                  <Stack spacing={1}>
                    {profile.location && (
                      <Box display="flex" alignItems="center" gap={1}>
                        <LocationOnIcon color="action" fontSize="small" />
                        <Typography variant="body2" color="text.secondary">
                          {profile.location}
                        </Typography>
                      </Box>
                    )}
                    
                    {profile.profession && (
                      <Box display="flex" alignItems="center" gap={1}>
                        <WorkIcon color="action" fontSize="small" />
                        <Typography variant="body2" color="text.secondary">
                          {profile.profession}
                        </Typography>
                      </Box>
                    )}
                    
                    {profile.education_level && (
                      <Box display="flex" alignItems="center" gap={1}>
                        <SchoolIcon color="action" fontSize="small" />
                        <Typography variant="body2" color="text.secondary">
                          {profile.education_level}
                        </Typography>
                      </Box>
                    )}
                  </Stack>

                  {/* Interests/Hobbies */}
                  {profile.hobbies && (
                    <Box mt={2}>
                      <Typography variant="subtitle2" gutterBottom>
                        Interests
                      </Typography>
                      <Box display="flex" gap={1} flexWrap="wrap">
                        {profile.hobbies.split(',').map((hobby, index) => (
                          <Chip
                            key={index}
                            label={hobby.trim()}
                            size="small"
                            sx={{ m: 0.5 }}
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                </CardContent>
                <CardActions>
                  <Button size="small" color="primary">
                    View Profile
                  </Button>
                  <Button size="small" color="primary">
                    Send Message
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* No results message */}
      {!loading && !message && recommendations.length === 0 && (
        <Box textAlign="center" mt={4}>
          <Typography variant="h6" color="text.secondary">
            No profiles found
          </Typography>
        </Box>
      )}
    </Box>
  );
}

export default RecommendationList;