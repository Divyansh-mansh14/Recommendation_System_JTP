const API_URL = 'http://127.0.0.1:8000/api';

// Helper function to handle API requests
const handleRequest = async (url, options = {}) => {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Origin': 'http://localhost:3000',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers,
  };

  try {
    const response = await fetch(url, { 
      ...options, 
      headers,
      credentials: 'include',
      mode: 'cors'
    });
    
    if (response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      throw new Error('Unauthorized');
    }

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Request failed');
    }

    return data;
  } catch (error) {
    console.error('API request error:', {
      url,
      error: error.message,
      status: error.response?.status,
      details: error.response?.data
    });
    throw error;
  }
};

// Auth endpoints
export const login = async (email, password) => {
  try {
    console.log('Starting login process...');
    
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    console.log('Sending login request to:', `${API_URL}/token`);
    const response = await fetch(`${API_URL}/token`, {
      method: 'POST',
      body: formData,
      credentials: 'include',
      mode: 'cors',
      headers: {
        'Accept': 'application/json',
        'Origin': 'http://localhost:3000'
      }
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Login failed');
    }
    
    console.log('Login response:', data);
    
    if (data.access_token) {
      console.log('Token received, storing in localStorage');
      localStorage.setItem('token', data.access_token);
      return data;
    }
    throw new Error('No token received');
  } catch (error) {
    console.error('Login error details:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
    });
    throw error;
  }
};

export const register = async (userData) => {
  try {
    console.log('Starting registration process...');
    console.log('User data:', userData);
    
    const response = await fetch(`${API_URL}/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'http://localhost:3000'
      },
      credentials: 'include',
      mode: 'cors',
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Registration failed:', {
        status: response.status,
        data: errorData
      });
      throw new Error(errorData.detail || 'Registration failed');
    }

    const data = await response.json();
    console.log('Registration response:', data);
    
    return data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

// Profile endpoints
export const getNextProfile = async () => {
  return handleRequest(`${API_URL}/profiles/next`);
};

export const recordSwipe = async (profileId, liked) => {
  return handleRequest(`${API_URL}/swipes`, {
    method: 'POST',
    body: JSON.stringify({
      swiped_id: profileId,
      liked: liked,
    }),
  });
};

export const getRecommendations = async () => {
  try {
    const response = await handleRequest(`${API_URL}/profiles/recommended`);
    if (!response || !response.data || !Array.isArray(response.data.profiles)) {
      throw new Error('Invalid response format from server');
    }
    return response;
  } catch (error) {
    console.error('Error in getRecommendations:', error);
    throw error;
  }
};

export const updateProfile = async (profileData) => {
  return handleRequest(`${API_URL}/profiles/me`, {
    method: 'PUT',
    body: JSON.stringify(profileData),
  });
};

export const getProfile = async () => {
  return handleRequest(`${API_URL}/profiles/me`);
}; 