# Recommendation System for JTP

A recommendation system built with FastAPI backend and React frontend, using MongoDB for data storage.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Windows Installation](#windows-installation)
  - [macOS Installation](#macos-installation)
  - [Using Docker](#using-docker)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm (comes with Node.js)
- MongoDB
- Git

## Installation

### Windows Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Recommendation-System-for-JTP
   ```

2. **Backend Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   .\venv\Scripts\activate

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend-react
   npm install
   ```

4. **MongoDB Setup**
   - Download and install MongoDB Community Server from the official website
   - Start MongoDB service

### macOS Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Recommendation-System-for-JTP
   ```

2. **Backend Setup**
   ```bash
   # Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend-react
   npm install
   ```

4. **MongoDB Setup**
   ```bash
   # Using Homebrew
   brew tap mongodb/brew
   brew install mongodb-community
   brew services start mongodb-community
   ```

### Using Docker

If you prefer using Docker:

```bash
# From the root directory
docker-compose up --build
```

This will start both the frontend and backend services together.

## Database Setup

The system comes with a pre-configured dataset in `app/matching_users_with_preferences_dataset.csv`. This data will be automatically loaded into MongoDB when you first run the application.

To verify the database population:
```bash
# From the root directory, with venv activated
python check_db.py
```

This will show you:
- Total number of users in the database
- Gender distribution of users
- Sample profiles
- Number of swipes

## Running the Application

### Windows

1. **Start Backend**
   ```bash
   # From the root directory, with venv activated
   python run.py
   ```

2. **Start Frontend**
   ```bash
   # In a new terminal, from the frontend-react directory
   npm start
   ```

### macOS

1. **Start Backend**
   ```bash
   # From the root directory, with venv activated
   python3 run.py
   ```

2. **Start Frontend**
   ```bash
   # In a new terminal, from the frontend-react directory
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Project Structure

```
.
├── app/                            # Backend application directory
│   ├── matching_users_with_preferences_dataset.csv  # Sample dataset
├── frontend-react/                 # Frontend React application
├── docker-compose.yml             # Docker compose configuration
├── requirements.txt               # Python dependencies
├── run.py                         # Backend server startup script
├── check_db.py                    # Database verification script
└── README.md                      # This file
```

## Technologies Used

- **Backend**:
  - FastAPI
  - MongoDB
  - Python 3.8+
  - Uvicorn
  - Pandas
  - Scikit-learn

- **Frontend**:
  - React
  - Node.js
  - npm

- **Database**:
  - MongoDB

- **Deployment**:
  - Docker
  - Docker Compose 