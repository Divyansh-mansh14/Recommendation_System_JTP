import React, { useState } from 'react';
import { ThemeProvider, CssBaseline, Container, Box } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import ProfileCards from './components/ProfileCards';
import MatchList from './components/MatchList';
import { AuthProvider } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import { useAuth } from './context/AuthContext';

// Theme with romantic color palette
const theme = createTheme({
  palette: {
    primary: {
      main: '#FF4B6E', 
      light: '#FF8199',
      dark: '#CC3C58',
    },
    secondary: {
      main: '#6B7FD7', 
    },
    background: {
      default: '#F8F9FB',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: '"Poppins", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

function AppContent() {
  const { token } = useAuth();

  return (
    <Router>
      <Routes>
        <Route path="/login" element={!token ? <LoginPage /> : <Navigate to="/profile-cards" />} />
        <Route path="/register" element={!token ? <RegisterPage /> : <Navigate to="/profile-cards" />} />
        <Route
          path="/profile-cards"
          element={
            token ? (
              <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
                <Header />
                <Container maxWidth="lg" sx={{ py: 4 }}>
                  <Box sx={{ display: 'flex', gap: 4 }}>
                    <Box sx={{ flex: 1 }}>
                      <ProfileCards />
                    </Box>
                    <Box sx={{ width: 320 }}>
                      <MatchList />
                    </Box>
                  </Box>
                </Container>
              </Box>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route path="/" element={<Navigate to={token ? "/profile-cards" : "/login"} />} />
      </Routes>
    </Router>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App; 