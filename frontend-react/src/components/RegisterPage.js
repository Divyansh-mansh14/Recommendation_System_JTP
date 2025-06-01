import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  MenuItem,
  Chip,
  Stack,
  Autocomplete,
  IconButton,
  Avatar,
} from '@mui/material';
import PhotoCamera from '@mui/icons-material/PhotoCamera';
import { register } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { fileToBase64, validateImage, compressImage } from '../utils/imageUtils';

// Constants for dropdown options
const RELIGIONS = [
  'Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Judaism', 
  'Sikhism', 'Atheism', 'Agnosticism', 'Other', 'Prefer not to say'
];

const EDUCATION_LEVELS = [
  'High School', 'Some College', 'Associate Degree', 'Bachelor\'s Degree',
  'Master\'s Degree', 'Doctorate', 'Professional Degree', 'Other'
];

const SMOKING_STATUS = [
  'Never', 'Occasionally', 'Regularly', 'Trying to quit', 'Prefer not to say'
];

const DRINKING_STATUS = [
  'Never', 'Socially', 'Occasionally', 'Regularly', 'Prefer not to say'
];

const DIET_PREFERENCES = [
  'Non-vegetarian', 'Vegetarian', 'Vegan', 'Pescatarian', 
  'Kosher', 'Halal', 'Other'
];

const COMMON_LANGUAGES = [
  'English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese',
  'Korean', 'Arabic', 'Hindi', 'Portuguese', 'Russian', 'Italian'
];

const COMMON_HOBBIES = [
  'Reading', 'Writing', 'Music', 'Gaming', 'Cooking', 'Travel',
  'Photography', 'Art', 'Sports', 'Fitness', 'Dancing', 'Movies',
  'Hiking', 'Yoga', 'Technology', 'Fashion', 'Gardening', 'Pets'
];

function RegisterPage({ onBackToLogin }) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    age: '',
    gender: '',
    preferred_gender: '',
    location: '',
    religion: '',
    education_level: '',
    profession: '',
    smoker: '',
    drinker: '',
    diet: '',
    hobbies: [],
    languages: [],
    profile_image: null,
  });
  const [previewImage, setPreviewImage] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      // Validate the image
      validateImage(file);

      // Convert to base64
      const base64String = await fileToBase64(file);
      
      // Compress the image
      const compressedImage = await compressImage(base64String);
      
      // Update form data and preview
      setFormData(prev => ({
        ...prev,
        profile_image: compressedImage
      }));
      setPreviewImage(compressedImage);
      
    } catch (error) {
      setError(error.message);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleArrayChange = (name) => (event, newValue) => {
    setFormData({
      ...formData,
      [name]: newValue,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('Submitting form data:', formData);
      
      // Validate required fields
      if (!formData.email || !formData.password || !formData.name || !formData.age || 
          !formData.gender || !formData.preferred_gender || !formData.location ||
          !formData.hobbies.length || !formData.languages.length) {
        throw new Error('Please fill in all required fields including hobbies and languages');
      }

      // Validate age
      const age = parseInt(formData.age, 10);
      if (isNaN(age) || age < 18 || age > 120) {
        throw new Error('Please enter a valid age between 18 and 120');
      }

      // Transform data to match backend schema
      const userData = {
        email: formData.email,
        password: formData.password,
        name: formData.name,
        age: age,
        gender: formData.gender.toLowerCase(),
        preferred_gender: formData.preferred_gender.toLowerCase(),
        location: formData.location,
        religion: formData.religion || null,
        education_level: formData.education_level || null,
        profession: formData.profession || null,
        smoking: formData.smoker === 'Regularly',
        drinking: formData.drinker === 'Regularly',
        diet: formData.diet || null,
        hobbies: formData.hobbies,
        languages: formData.languages,
        profile_image: formData.profile_image || null
      };

      console.log('Submitting user data:', userData);
      const response = await register(userData);
      console.log('Registration response:', response);
      
      // Clear form data
      setFormData({
        email: '',
        password: '',
        name: '',
        age: '',
        gender: '',
        preferred_gender: '',
        location: '',
        religion: '',
        education_level: '',
        profession: '',
        smoker: '',
        drinker: '',
        diet: '',
        hobbies: [],
        languages: [],
        profile_image: null,
      });
      
      onBackToLogin();
    } catch (error) {
      console.error('Registration error:', error);
      setError(error.response?.data?.detail || error.message || 'Failed to create account. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        p: 2,
      }}
    >
      <Card sx={{ maxWidth: 600, width: '100%', my: 4 }}>
        <CardContent sx={{ p: 4 }}>
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant="h4" component="h1" color="primary" gutterBottom>
              Create Account
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Join DateMate and find your perfect match
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <Stack spacing={2}>
              {/* Profile Image Upload */}
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
                <Avatar
                  src={previewImage}
                  sx={{
                    width: 120,
                    height: 120,
                    mb: 2,
                    bgcolor: 'grey.300',
                  }}
                />
                <Button
                  variant="outlined"
                  component="label"
                  startIcon={<PhotoCamera />}
                  sx={{ mb: 1 }}
                >
                  Upload Photo
                  <input
                    type="file"
                    hidden
                    accept="image/*"
                    onChange={handleImageUpload}
                  />
                </Button>
                <Typography variant="caption" color="text.secondary">
                  Max size: 5MB. Formats: JPG, PNG, GIF
                </Typography>
              </Box>

              {/* Basic Information */}
              <Typography variant="h6" color="primary" gutterBottom>
                Basic Information
              </Typography>
              <TextField
                fullWidth
                label="Email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <TextField
                fullWidth
                label="Password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
              <TextField
                fullWidth
                label="Full Name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
              <TextField
                fullWidth
                label="Age"
                name="age"
                type="number"
                value={formData.age}
                onChange={handleChange}
                required
              />

              {/* Personal Details */}
              <Typography variant="h6" color="primary" gutterBottom sx={{ mt: 2 }}>
                Personal Details
              </Typography>
              <TextField
                select
                fullWidth
                label="Gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                required
              >
                <MenuItem value="male">Male</MenuItem>
                <MenuItem value="female">Female</MenuItem>
                <MenuItem value="other">Other</MenuItem>
              </TextField>
              <TextField
                select
                fullWidth
                label="Interested In"
                name="preferred_gender"
                value={formData.preferred_gender}
                onChange={handleChange}
                required
              >
                <MenuItem value="male">Male</MenuItem>
                <MenuItem value="female">Female</MenuItem>
                <MenuItem value="other">Any</MenuItem>
              </TextField>
              <TextField
                fullWidth
                label="Location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                required
              />

              {/* Background */}
              <Typography variant="h6" color="primary" gutterBottom sx={{ mt: 2 }}>
                Background
              </Typography>
              <TextField
                select
                fullWidth
                label="Religion"
                name="religion"
                value={formData.religion}
                onChange={handleChange}
              >
                {RELIGIONS.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
              <TextField
                select
                fullWidth
                label="Education Level"
                name="education_level"
                value={formData.education_level}
                onChange={handleChange}
              >
                {EDUCATION_LEVELS.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
              <TextField
                fullWidth
                label="Profession"
                name="profession"
                value={formData.profession}
                onChange={handleChange}
              />

              {/* Lifestyle */}
              <Typography variant="h6" color="primary" gutterBottom sx={{ mt: 2 }}>
                Lifestyle
              </Typography>
              <TextField
                select
                fullWidth
                label="Smoking Status"
                name="smoker"
                value={formData.smoker}
                onChange={handleChange}
              >
                {SMOKING_STATUS.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
              <TextField
                select
                fullWidth
                label="Drinking Status"
                name="drinker"
                value={formData.drinker}
                onChange={handleChange}
              >
                {DRINKING_STATUS.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>
              <TextField
                select
                fullWidth
                label="Diet Preference"
                name="diet"
                value={formData.diet}
                onChange={handleChange}
              >
                {DIET_PREFERENCES.map((option) => (
                  <MenuItem key={option} value={option}>
                    {option}
                  </MenuItem>
                ))}
              </TextField>

              {/* Interests and Skills */}
              <Typography variant="h6" color="primary" gutterBottom sx={{ mt: 2 }}>
                Interests and Skills
              </Typography>
              <Autocomplete
                multiple
                options={COMMON_HOBBIES}
                value={formData.hobbies}
                onChange={handleArrayChange('hobbies')}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Hobbies"
                    placeholder="Select your hobbies"
                    required
                    error={formData.hobbies.length === 0}
                    helperText={formData.hobbies.length === 0 ? "Please select at least one hobby" : ""}
                  />
                )}
                renderTags={(value, getTagProps) =>
                  value.map((option, index) => {
                    const { key, ...chipProps } = getTagProps({ index });
                    return (
                      <Chip
                        key={key}
                        label={option}
                        {...chipProps}
                        color="primary"
                        variant="outlined"
                      />
                    );
                  })
                }
              />
              <Autocomplete
                multiple
                options={COMMON_LANGUAGES}
                value={formData.languages}
                onChange={handleArrayChange('languages')}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    label="Languages Known"
                    placeholder="Select languages"
                    required
                    error={formData.languages.length === 0}
                    helperText={formData.languages.length === 0 ? "Please select at least one language" : ""}
                  />
                )}
                renderTags={(value, getTagProps) =>
                  value.map((option, index) => {
                    const { key, ...chipProps } = getTagProps({ index });
                    return (
                      <Chip
                        key={key}
                        label={option}
                        {...chipProps}
                        color="primary"
                        variant="outlined"
                      />
                    );
                  })
                }
              />

              {/* Submit Buttons */}
              <Button
                fullWidth
                variant="contained"
                size="large"
                type="submit"
                disabled={loading}
                sx={{ mt: 3 }}
              >
                {loading ? 'Creating Account...' : 'Create Account'}
              </Button>
              <Button
                fullWidth
                variant="text"
                onClick={onBackToLogin}
              >
                Back to Login
              </Button>
            </Stack>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
}

export default RegisterPage; 