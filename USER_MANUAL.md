# User Manual

This manual provides instructions on how to use the Recommendation System for JTP.

## Getting Started

1. **Accessing the Application**
   - Open your web browser
   - Navigate to http://localhost:3000
   - The backend API is available at http://localhost:8000

2. **System Requirements**
   - Modern web browser (Chrome, Firefox, Safari, Edge)
   - Internet connection
   - Minimum screen resolution: 1024x768

## Features

### 1. User Profile Management

- **View Profile**
  - Access your profile information
  - View your preferences
  - Check your match history

- **Update Preferences**
  - Set gender preferences
  - Update profile information

### 2. Recommendation System

- **Profile Recommendations**
  - View recommended profiles
  - Swipe right to like
  - Swipe left to pass

- **Matching System**
  - Get notified when you match with someone
  - View your matches

### 3. Database Statistics

You can check the system statistics using the database verification tool:
```bash
python check_db.py
```

This will show:
- Total number of users
- Gender distribution
- Sample profiles
- Number of swipes

## Docker Deployment

### Prerequisites
- Docker Desktop installed on your machine
- Docker Compose installed
- Git (to clone the repository)

### Running with Docker

1. **Build and Start Containers**
   ```bash
   # From the project root directory
   docker-compose up --build
   ```
   This command will:
   - Build the frontend container
   - Build the backend container
   - Start MongoDB container
   - Set up the network between containers
   - Mount necessary volumes

2. **Verify Containers**
   ```bash
   # Check running containers
   docker ps
   ```
   You should see three containers running:
   - frontend-react container
   - backend container
   - mongodb container

3. **Accessing the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - MongoDB: localhost:27017 (internal access)

### Docker Commands Reference

1. **Start Containers in Background**
   ```bash
   docker-compose up -d
   ```

2. **Stop Containers**
   ```bash
   docker-compose down
   ```

3. **View Container Logs**
   ```bash
   # All containers
   docker-compose logs

   # Specific container
   docker-compose logs frontend
   docker-compose logs backend
   docker-compose logs mongodb
   ```

4. **Rebuild Containers**
   ```bash
   # If you make changes to the code
   docker-compose up --build
   ```

5. **Clean Up**
   ```bash
   # Remove containers and networks
   docker-compose down

   # Remove containers, networks, and volumes
   docker-compose down -v
   ```

### Troubleshooting Docker Issues

1. **Container Not Starting**
   - Check Docker logs: `docker-compose logs`
   - Verify port availability
   - Ensure Docker Desktop is running

2. **Database Connection Issues**
   - Check if MongoDB container is running
   - Verify network connectivity between containers
   - Check MongoDB logs: `docker-compose logs mongodb`

3. **Frontend Not Accessible**
   - Verify frontend container is running
   - Check container logs
   - Ensure port 3000 is not in use

## API Endpoints

The backend API is available at http://localhost:8000 with the following endpoints:

1. **User Management**
   - GET /users/ - List all users
   - GET /users/{user_id} - Get specific user
   - POST /users/ - Create new user
   - PUT /users/{user_id} - Update user

2. **Recommendations**
   - GET /recommendations/{user_id} - Get recommendations for user
   - POST /swipes/ - Record a swipe action

3. **Matches**
   - GET /matches/{user_id} - Get user matches

## Common Operations

### How to Start Using the System

1. Access the application at http://localhost:3000
2. Create or update your profile
3. Set your preferences
4. Start receiving recommendations

### Viewing Recommendations

1. Navigate to the main page
2. View recommended profiles
3. Swipe right to like, left to pass
4. Check your matches in the matches section

## Troubleshooting

### Common Issues

1. **Can't See Recommendations**
   - Ensure your preferences are set
   - Check if there are available profiles matching your criteria
   - Verify backend connection

2. **Application Not Loading**
   - Check if frontend is running (http://localhost:3000)
   - Verify backend is running (http://localhost:8000)
   - Ensure MongoDB service is active

3. **Match Notifications Not Working**
   - Refresh the page
   - Check your browser notifications settings
   - Verify backend connection 