# Installation Manual

This guide provides detailed installation instructions for both Windows and macOS systems.

## Prerequisites

Before installing the application, ensure you have the following prerequisites installed:

- Python 3.8 or higher
- Node.js 16 or higher
- npm (comes with Node.js)
- MongoDB
- Git

## Detailed Installation Steps

### Windows Installation

1. **Install Prerequisites**
   - Download and install Python from [python.org](https://python.org)
   - Download and install Node.js from [nodejs.org](https://nodejs.org)
   - Download and install MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Download and install Git from [git-scm.com](https://git-scm.com)

2. **Clone the Repository**
   ```bash
   git clone <https://github.com/Divyansh-mansh14/Recommendation_System_JTP.git>
   cd Recommendation-System-for-JTP
   ```

3. **Set Up Python Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   .\venv\Scripts\activate

   # Install Python dependencies
   pip install -r requirements.txt
   ```

4. **Set Up Frontend**
   ```bash
   # Navigate to frontend directory
   cd frontend-react

   # Install dependencies
   npm install

   # Return to root directory
   cd ..
   ```

5. **Configure MongoDB**
   - Start MongoDB service:
     1. Open Services (services.msc)
     2. Find MongoDB
     3. Start the service
   - Verify MongoDB is running:
     ```bash
     mongo --eval "db.version()"
     ```

### macOS Installation

1. **Install Prerequisites**
   ```bash
   # Install Homebrew if not installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install Python
   brew install python@3.8

   # Install Node.js
   brew install node

   # Install MongoDB
   brew tap mongodb/brew
   brew install mongodb-community
   ```

2. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Recommendation-System-for-JTP
   ```

3. **Set Up Python Virtual Environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate virtual environment
   source venv/bin/activate

   # Install Python dependencies
   pip install -r requirements.txt
   ```

4. **Set Up Frontend**
   ```bash
   # Navigate to frontend directory
   cd frontend-react

   # Install dependencies
   npm install

   # Return to root directory
   cd ..
   ```

5. **Start MongoDB Service**
   ```bash
   brew services start mongodb-community
   ```

## Docker Installation (Alternative)

If you prefer using Docker:

1. **Install Docker**
   - Windows: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - macOS: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

## Database Setup

The application uses a pre-configured dataset located at `app/matching_users_with_preferences_dataset.csv`.

1. **Verify MongoDB Connection**
   ```bash
   # From project root, with venv activated
   python check_db.py
   ```

2. **Expected Output**
   The script will show:
   - Total users in database
   - Gender distribution
   - Sample profiles
   - Number of swipes

## Troubleshooting

1. **MongoDB Connection Issues**
   - Ensure MongoDB service is running
   - Check if port 27017 is available
   - Verify MongoDB installation: `mongo --version`

2. **Python Dependencies Issues**
   - Ensure virtual environment is activated
   - Try upgrading pip: `python -m pip install --upgrade pip`
   - Install dependencies one by one if bulk install fails

3. **Node.js/npm Issues**
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install` 
