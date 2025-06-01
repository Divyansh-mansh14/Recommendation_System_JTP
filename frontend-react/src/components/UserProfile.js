import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Avatar,
  Grid,
  Chip,
  IconButton,
  Paper,
  CircularProgress,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import SchoolIcon from '@mui/icons-material/School';
import WorkIcon from '@mui/icons-material/Work';
import TranslateIcon from '@mui/icons-material/Translate';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import SmokingRoomsIcon from '@mui/icons-material/SmokingRooms';
import LocalBarIcon from '@mui/icons-material/LocalBar';

function UserProfile({ open, onClose, userData }) {
  if (!open) return null;

  if (!userData) {
    return (
      <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          My Profile
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
        <DialogContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
          <CircularProgress />
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle sx={{ m: 0, p: 2 }}>
        My Profile
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
      <DialogContent dividers>
        <Grid container spacing={3}>
          {/* Profile Image */}
          <Grid item xs={12} display="flex" justifyContent="center">
            <Avatar
              alt={userData.name || 'User'}
              src={userData.profile_image}
              sx={{ width: 150, height: 150 }}
            />
          </Grid>

          {/* Basic Info */}
          <Grid item xs={12}>
            <Typography variant="h5" gutterBottom align="center">
              {userData.name || 'No Name'}{userData.age ? `, ${userData.age}` : ''}
            </Typography>
            {userData.location && (
              <Typography variant="body1" color="text.secondary" align="center" gutterBottom>
                <Box display="flex" alignItems="center" justifyContent="center" gap={1}>
                  <LocationOnIcon fontSize="small" />
                  {userData.location}
                </Box>
              </Typography>
            )}
          </Grid>

          {/* Professional Info */}
          {(userData.profession || userData.education_level) && (
            <Grid item xs={12}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Professional Details
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {userData.profession && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <WorkIcon fontSize="small" color="action" />
                      <Typography variant="body1">
                        {userData.profession}
                      </Typography>
                    </Box>
                  )}
                  {userData.education_level && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <SchoolIcon fontSize="small" color="action" />
                      <Typography variant="body1">
                        {userData.education_level}
                      </Typography>
                    </Box>
                  )}
                </Box>
              </Paper>
            </Grid>
          )}

          {/* Lifestyle */}
          {(userData.religion || userData.diet || userData.smoker || userData.drinker) && (
            <Grid item xs={12}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Lifestyle
                </Typography>
                <Grid container spacing={2}>
                  {userData.religion && (
                    <Grid item xs={12} sm={6}>
                      <Typography variant="body2" color="text.secondary">
                        Religion: {userData.religion}
                      </Typography>
                    </Grid>
                  )}
                  {userData.diet && (
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <RestaurantIcon fontSize="small" color="action" />
                        <Typography variant="body2" color="text.secondary">
                          Diet: {userData.diet}
                        </Typography>
                      </Box>
                    </Grid>
                  )}
                  {userData.smoker && (
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <SmokingRoomsIcon fontSize="small" color="action" />
                        <Typography variant="body2" color="text.secondary">
                          Smoking: {userData.smoker}
                        </Typography>
                      </Box>
                    </Grid>
                  )}
                  {userData.drinker && (
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LocalBarIcon fontSize="small" color="action" />
                        <Typography variant="body2" color="text.secondary">
                          Drinking: {userData.drinker}
                        </Typography>
                      </Box>
                    </Grid>
                  )}
                </Grid>
              </Paper>
            </Grid>
          )}

          {/* Languages */}
          {userData.languages && userData.languages.length > 0 && (
            <Grid item xs={12}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <TranslateIcon color="primary" />
                  <Typography variant="subtitle1">
                    Languages
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {userData.languages.map((language, index) => (
                    <Chip
                      key={index}
                      label={language}
                      color="secondary"
                      variant="outlined"
                      size="small"
                    />
                  ))}
                </Box>
              </Paper>
            </Grid>
          )}

          {/* Hobbies */}
          {userData.hobbies && userData.hobbies.length > 0 && (
            <Grid item xs={12}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="subtitle1" gutterBottom>
                  Hobbies & Interests
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {userData.hobbies.map((hobby, index) => (
                    <Chip
                      key={index}
                      label={hobby}
                      color="primary"
                      variant="outlined"
                      size="small"
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

export default UserProfile; 