
# Elder Care Management System

The Elder Care Management System is an innovative and user-friendly platform designed to enhance the quality of life for elderly individuals while simplifying care management for families, guardians, caregivers, and elder care facilities.

## 🎨 Application Design

### Modern Frontend (React)
![React application design](react-frontend/src/media/ApplicationDesign.png)

### Legacy Frontend (Streamlit)
![application design](frontend/media/ApplicationDesign.png)


## ✨ Features
1. 🛠️ Manage caregivers, elderly individuals, tasks, and medications.
2. 📝 Generate a PDF payment report for caregivers.
3. 🔄 Assign and unassign caregivers to elderly individuals.
4. 🏥 View comprehensive caregiver and elderly profiles
5. 🚀 Flexible and extensible design for future enhancements.
6. 🎨 **NEW**: Modern React frontend with Tailwind CSS (under development)

## 📂 Project Structure
```
Elder-Care/
│── backend/
│   │── db/                # Database configuration and connection
│   │   │── __init__.py
│   │   │── database.py
│   │
│   │── models/            # SQLAlchemy models for database
│   │   │── __init__.py
│   │   │── caregiver.py
│   │   │── caregiver_assignments.py
│   │   │── elderly.py
│   │   │── medication.py
│   │   │── task.py
│   │   │── user.py
│   │
│   │── routes/            # FastAPI route handlers
│   │   │── __init__.py
│   │   │── auth.py
│   │   │── caregiver_assignments.py
│   │   │── caregivers.py
│   │   │── elderly.py
│   │
│   │── services/          # Business logic layer with Redis caching
│   │   │── __init__.py
│   │   │── auth_service.py
│   │   │── elderly_service.py
│   │   │── caregiver_service.py
│   │   │── caregiver_assignment_service.py
│   │
│   │── schemas/           # Pydantic schemas for data validation
│   │   │── __init__.py
│   │   │── auth.py
│   │   │── caregiver.py
│   │   │── caregiver_assignment.py
│   │   │── elderly.py
│   │   │── medication.py
│   │   │── task.py
│   │
│   │── utils/             # Utility functions (e.g., PDF generation, Redis caching)
│   │   │── __init__.py
│   │   │── pdf_generator.py
│   │   │── redis_cache.py
│   │
│   │── Tests/             # Automated test scripts
│   │   │── test_api_integration.py
│   │   │── test_units.py
│   │
│   │── Dockerfile         # Backend containerization
│   │── main.py            # FastAPI application entry point
│   │── requirements.txt   # Backend dependencies
│
│── frontend/               # Legacy Streamlit frontend
│   │── components/        # Streamlit UI components
│   │   │── __init__.py
│   │   │── add_data.py
│   │   │── auth_ui.py
│   │   │── manage_caregivers.py
│   │   │── manage_elderly.py
│   │   │── view_data.py
│   │── media/            # Media assets and images
│   │   │── ApplicationDesign.png  # Streamlit application design
│   │── Dockerfile         # Frontend containerization
│   │── api_client.py      # Handles API communication
│   │── requirements.txt   # Frontend dependencies
│   │── ui.py              # Streamlit main UI file
│
│── react-frontend/         # 🆕 Modern React frontend (under development)
│   │── src/               # React source code
│   │   │── components/    # React components
│   │   │   │── Header.js  # Responsive navigation header with mobile menu
│   │   │   │── CaregiverDashboard.js  # Caregiver dashboard page
│   │   │── media/         # Media assets and images
│   │   │   │── ApplicationDesign.png  # React application design
│   │   │── App.js         # Main App component with React Router
│   │   │── App.css        # App styles
│   │   │── App.test.js    # App tests
│   │   │── index.js       # Entry point
│   │   │── index.css      # Tailwind CSS imports
│   │   │── logo.svg       # React logo
│   │   │── reportWebVitals.js # Performance monitoring
│   │   │── setupTests.js  # Test configuration
│   │
│   │── public/            # Static assets
│   │   │── index.html     # HTML template
│   │   │── favicon.ico    # Browser icon
│   │   │── manifest.json  # PWA manifest
│   │   │── robots.txt     # SEO configuration
│   │   │── logo192.png    # App logo (192x192)
│   │   │── logo512.png    # App logo (512x512)
│   │
│   │── package.json       # Node.js dependencies
│   │── package-lock.json  # Locked dependency versions
│   │── tailwind.config.js # Tailwind CSS configuration
│   │── postcss.config.js  # PostCSS configuration
│   │── README.md          # React app documentation
│
│── docker-compose.yml     # Docker configuration for services
│── README.md              # Project documentation
│── pytest.ini             # Pytest configuration
```

## 💻 Technologies Used

### Backend
- **FastAPI**: Backend framework.
- **PostgreSQL**: Primary database (production).
- **SQLite**: Test database.
- **Redis**: Caching layer for improved performance.
- **Docker**: Containerization.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation and settings management.
- **FPDF**: PDF generation.
- **pytest**: Testing framework.
- **JWT (python-jose)**: Authentication token handling.
- **Passlib with bcrypt**: Secure password hashing.
- **Uvicorn**: ASGI server for running FastAPI.
- **Python-dotenv**: Environment variable management.
- **Pytest-asyncio**: Async testing support.

### Frontend
- **Streamlit**: Legacy UI framework (fully functional)
- **React**: Modern frontend framework (🚧 under development)
- **Tailwind CSS**: Utility-first CSS framework for React
- **PostCSS**: CSS processing for React
- **Axios**: HTTP client for API communication
- **React Router**: Client-side routing for single-page application

## 🎥 Demo Video

[![Watch the video](https://img.youtube.com/vi/5YUIZpneDnw/hqdefault.jpg)](https://youtu.be/5YUIZpneDnw)

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/EASS-HIT-PART-A-2024-CLASS-VI/Elder-Care.git
```

---

### Step 2: Navigate to the Project Directory
```bash
cd Elder-Care
```

### Step 3: Create a `.env` File
Create a `.env` file in the project's root directory and add the following variables:
```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=elder_care_db
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/elder_care_db
```

### Step 4: Build and Run the Application with Docker
```bash
docker-compose up --build
```

### Step 5: Access the Application UI
Once the application is running, you can access the UI of the Elder Care Management System in your web browser:

**Legacy Frontend (Streamlit):**  
- **URL**: [http://localhost:8501](http://localhost:8501)  
  - Manage caregivers and their salaries, and generate a detailed PDF including all caregiver details and payment information."  
  - Manage elderly individuals, their tasks, and medications.  
  - View all data in a structured and user-friendly format.  

**🆕 Modern Frontend (React) - Under Development:**  
- **URL**: [http://localhost:3000](http://localhost:3000)  
  - Modern, responsive UI built with React and Tailwind CSS
  - Enhanced user experience with component-based architecture
  - Currently in development phase

**Backend API (Swagger Documentation):**  
- **URL**: [http://localhost:8000/docs](http://localhost:8000/docs)  
  - Provides API documentation and allows you to test the backend endpoints directly.  

## 🆕 React Frontend Development

### Current Status: 🚧 Under Development

The React frontend is currently being developed to provide a modern, scalable alternative to the Streamlit interface.

### ✅ **Recently Completed Features:**
- **Responsive Header Component** - Blue-themed header with hospital logo
- **Mobile Navigation** - Hamburger menu with collapsible navigation
- **React Router Setup** - Page navigation between welcome screen and dashboard
- **Component Architecture** - Modular, reusable React components
- **Tailwind CSS Integration** - Mobile-first responsive design
- **State Management** - useState hook for mobile menu functionality

### 🚧 **Features in Development:**
- **Modern UI/UX**: Built with React 18 and Tailwind CSS
- **Component Architecture**: Reusable, maintainable components
- **Responsive Design**: Mobile-first approach
- **API Integration**: Seamless communication with FastAPI backend
- **State Management**: Efficient data handling and caching

### 🎯 **Current Navigation Structure:**
- **Welcome Screen** - Home page with app introduction
- **Caregiver Dashboard** - View and manage all caregivers
- **Elder Dashboard** - View and manage all elderly clients
- **Manage Caregivers** - Add/edit/delete caregiver forms
- **Manage Elderly** - Add/edit/delete elderly client forms

### Development Setup:
```bash
# Navigate to React frontend
cd react-frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Tech Stack:
- **React 18**: Latest React features and hooks
- **Tailwind CSS v3**: Utility-first CSS framework
- **PostCSS**: CSS processing and optimization
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls

## 🧪 Testing

The project includes comprehensive automated tests that run inside Docker containers to ensure proper access to Redis cache and PostgreSQL database.

### Running Tests

**Prerequisites:**
- Make sure Docker containers are running: `docker-compose up`
- All services (backend, database, Redis) must be active

**Run All Tests:**
```bash
docker-compose exec backend python -m pytest Tests/ -v
```

**Run Specific Test File:**
```bash
docker-compose exec backend python -m pytest Tests/test_api_integration.py -v
```

**Run Specific Test:**
```bash
docker-compose exec backend python -m pytest Tests/test_api_integration.py::test_add_caregiver_success -v
```

**Run Tests with Coverage:**
```bash
docker-compose exec backend python -m pytest Tests/ --cov=. --cov-report=term-missing
```

### Test Structure

- **`test_api_integration.py`**: Integration tests for API endpoints
  - Tests all CRUD operations for caregivers, elderly, tasks, medications
  - Tests caregiver assignments functionality
  - Tests error handling and edge cases

- **`test_units.py`**: Unit tests for data models
  - Tests Caregiver, Elderly, and Task model functionality
  - Tests salary calculations and data validation

### Why Run Tests in Docker?

- **Redis Access**: Tests need access to Redis cache running in Docker
- **Database Access**: Tests need access to PostgreSQL database
- **Consistent Environment**: Ensures tests run in the same environment as the application
- **Service Dependencies**: All required services (Redis, PostgreSQL) are available

### Test Results

When tests pass successfully, you should see output like:
```
======================================================== test session starts =========================================================
platform linux -- Python 3.10.18, pytest-8.4.1, pluggy-1.6.0
collected 26 items

Tests/test_api_integration.py::test_add_caregiver_success PASSED
Tests/test_api_integration.py::test_add_existing_caregiver PASSED
...
Tests/test_units.py::test_update_task_status PASSED

========================================================= 26 passed in 2.97s =========================================================
```

## 🔄 Migration Strategy

### Current State:
- **Streamlit Frontend**: Fully functional, production-ready
- **React Frontend**: Under active development with working navigation

### Migration Plan:
1. **Phase 1**: Complete React frontend development ✅ **IN PROGRESS**
2. **Phase 2**: Feature parity with Streamlit version
3. **Phase 3**: User testing and feedback
4. **Phase 4**: Gradual migration of users
5. **Phase 5**: Deprecate Streamlit frontend (optional)

### Benefits of React Migration:
- **Better Performance**: Faster rendering and updates
- **Enhanced UX**: Modern, responsive interface
- **Maintainability**: Component-based architecture
- **Scalability**: Easier to add new features
- **Portfolio Value**: Industry-standard technology stack

## 📬 Contact Info
**Ori Levi**  
📧 Email: Leviori1218@gmail.com  
🐙 GitHub: [OriLevi12](https://github.com/OriLevi12)
