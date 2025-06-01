import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Avatar,
  Chip,
  Divider,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Grid,
  Paper,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { getRecommendations } from '../services/api';
import { useAuth } from '../context/AuthContext';

const getHobbiesArray = (profile) => {
  if (!profile.hobbies) return [];
  if (Array.isArray(profile.hobbies)) return profile.hobbies;
  if (typeof profile.hobbies === 'string') return profile.hobbies.split(',').map(h => h.trim());
  return [];
};

const getLanguagesArray = (profile) => {
  if (!profile.languages) return [];
  if (Array.isArray(profile.languages)) return profile.languages;
  if (typeof profile.languages === 'string') return profile.languages.split(',').map(l => l.trim());
  return [];
};

function ProfileDialog({ profile, photo, open, onClose }) {
  if (!profile) return null;
  
  const languages = getLanguagesArray(profile);
  const hobbies = getHobbiesArray(profile);
  
  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle sx={{ m: 0, p: 2 }}>
        Profile Details
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={3}>
          {/* Profile Image */}
          <Grid item xs={12} display="flex" justifyContent="center">
            <Avatar
              alt={profile.name}
              src={photo}
              sx={{ width: 150, height: 150 }}
            />
          </Grid>

          {/* Basic Info */}
          <Grid item xs={12}>
            <Typography variant="h5" gutterBottom align="center">
              {profile.name}, {profile.age}
            </Typography>
            <Typography variant="body1" color="text.secondary" align="center" gutterBottom>
              {profile.location}
            </Typography>
          </Grid>

          {/* Professional Info */}
          {(profile.profession || profile.education_level) && (
            <Grid item xs={12}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Professional Details
                </Typography>
                {profile.profession && (
                  <Typography variant="body1" color="text.secondary" paragraph>
                    {profile.profession}
                  </Typography>
                )}
                {profile.education_level && (
                  <Typography variant="body1" color="text.secondary">
                    Education: {profile.education_level}
                  </Typography>
                )}
              </Paper>
            </Grid>
          )}

          {/* Lifestyle */}
          {(profile.religion || profile.diet || profile.smoker || profile.drinker) && (
            <Grid item xs={12}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Lifestyle
                </Typography>
                <Grid container spacing={2}>
                  {profile.religion && (
                    <Grid item xs={12} sm={6}>
                      <Typography variant="body2" color="text.secondary">
                        Religion: {profile.religion}
                      </Typography>
                    </Grid>
                  )}
                  {profile.diet && (
                    <Grid item xs={12} sm={6}>
                      <Typography variant="body2" color="text.secondary">
                        Diet: {profile.diet}
                      </Typography>
                    </Grid>
                  )}
                  {profile.smoker && (
                    <Grid item xs={12} sm={6}>
                      <Typography variant="body2" color="text.secondary">
                        Smoking: {profile.smoker}
                      </Typography>
                    </Grid>
                  )}
                  {profile.drinker && (
                    <Grid item xs={12} sm={6}>
                      <Typography variant="body2" color="text.secondary">
                        Drinking: {profile.drinker}
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </Paper>
            </Grid>
          )}

          {/* Languages */}
          {languages.length > 0 && (
            <Grid item xs={12}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Languages
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {languages.map((language, index) => (
                    <Chip
                      key={index}
                      label={language}
                      size="small"
                      color="secondary"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Paper>
            </Grid>
          )}

          {/* Hobbies */}
          {hobbies.length > 0 && (
            <Grid item xs={12}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Hobbies & Interests
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {hobbies.map((hobby, index) => (
                    <Chip
                      key={index}
                      label={hobby}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </Paper>
            </Grid>
          )}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
}

function MatchList() {
  const { token } = useAuth();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [profilePhotos, setProfilePhotos] = useState({});

  const handleProfileClick = (profile) => {
    setSelectedProfile(profile);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setSelectedProfile(null);
  };

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getRecommendations();
      
      if (!response || !response.data || !Array.isArray(response.data.profiles)) {
        throw new Error('Invalid response format from server');
      }
      
      // Ensure hobbies and languages are in the correct format for each profile
      const processedData = response.data.profiles.map(profile => ({
        ...profile,
        hobbies: getHobbiesArray(profile),
        languages: getLanguagesArray(profile)
      }));
      
      setMatches(processedData);
      
      // Initialize profile photos
      const photos = {};
      processedData.forEach(profile => {
        photos[profile._id] = profile.profile_image || `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.name)}&background=random&size=150`;
      });
      setProfilePhotos(photos);
      
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      if (error.message.includes('Unauthorized')) {
        setError({
          type: 'error',
          message: 'Please log in to view recommendations',
          details: 'Your session may have expired'
        });
      } else if (error.message.includes('No more profiles')) {
        setError({
          type: 'info',
          message: 'No recommendations available',
          details: 'Try adjusting your preferences or check back later'
        });
      } else {
        setError({
          type: 'error',
          message: 'Unable to load recommendations',
          details: error.message
        });
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchRecommendations();
    }
  }, [token]);

  if (loading) {
    return (
      <Card sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress />
      </Card>
    );
  }

  if (error) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Matches & Recommendations
          </Typography>
          <Alert 
            severity={error.type} 
            sx={{ mb: 2 }}
            action={
              error.type === 'info' && (
                <Button color="inherit" size="small" onClick={() => window.location.reload()}>
                  Refresh
                </Button>
              )
            }
          >
            {error.message}
          </Alert>
          {error.details && (
            <Typography variant="body2" color="text.secondary">
              {error.details}
            </Typography>
          )}
        </CardContent>
      </Card>
    );
  }

  if (!matches.length) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Matches & Recommendations
          </Typography>
          <Alert severity="info">
            Start swiping to get matches and recommendations!
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Matches & Recommendations
          </Typography>
          <List sx={{ width: '100%', bgcolor: 'background.paper' }}>
            {matches.map((match, index) => {
              const hobbies = getHobbiesArray(match);
              return (
                <React.Fragment key={match._id}>
                  {index > 0 && <Divider variant="inset" component="li" />}
                  <ListItem 
                    alignItems="flex-start"
                    sx={{
                      '&:hover': {
                        bgcolor: 'action.hover',
                      },
                      cursor: 'pointer'
                    }}
                    onClick={() => handleProfileClick(match)}
                  >
                    <ListItemAvatar>
                      <Avatar
                        alt={match.name}
                        src={profilePhotos[match._id]}
                      />
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Typography
                          component="span"
                          variant="subtitle1"
                          color="text.primary"
                        >
                          {match.name}, {match.age}
                        </Typography>
                      }
                      secondary={
                        <React.Fragment>
                          <Typography
                            component="span"
                            variant="body2"
                            color="text.primary"
                          >
                            {match.location}
                          </Typography>
                          {match.profession && (
                            <Typography
                              component="div"
                              variant="body2"
                              color="text.secondary"
                              sx={{ mt: 0.5 }}
                            >
                              {match.profession}
                            </Typography>
                          )}
                          {hobbies.length > 0 && (
                            <Box sx={{ mt: 1 }}>
                              {hobbies.slice(0, 3).map((hobby, idx) => (
                                <Chip
                                  key={`${match._id}-${idx}-${hobby}`}
                                  label={hobby}
                                  size="small"
                                  sx={{ mr: 0.5, mb: 0.5 }}
                                />
                              ))}
                              {hobbies.length > 3 && (
                                <Chip
                                  label={`+${hobbies.length - 3}`}
                                  size="small"
                                  variant="outlined"
                                />
                              )}
                            </Box>
                          )}
                        </React.Fragment>
                      }
                    />
                  </ListItem>
                </React.Fragment>
              );
            })}
          </List>
        </CardContent>
      </Card>

      <ProfileDialog
        profile={selectedProfile}
        photo={selectedProfile ? profilePhotos[selectedProfile._id] : null}
        open={dialogOpen}
        onClose={handleCloseDialog}
      />
    </>
  );
}

export default MatchList; 