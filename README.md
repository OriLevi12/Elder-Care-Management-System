
# Elder Care Management System

The Elder Care Management System is an innovative and user-friendly platform designed to enhance the quality of life for elderly individuals while simplifying care management for families, guardians, caregivers, and elder care facilities.


## ✨ Features
1. 🛠️ Manage caregivers, elderly individuals, tasks, and medications.
2. 📝 Generate a PDF payment report for caregivers.
3. 🔄 Assign and unassign caregivers to elderly individuals.
4. 🏥 View comprehensive caregiver and elderly profiles
5. 🚀 Flexible and extensible design for future enhancements.


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
│   │   │── caregiver_assignments.py
│   │   │── caregivers.py
│   │   │── elderly.py
│   │
│   │── services/          # Business logic layer with Redis caching
│   │   │── __init__.py
│   │   │── elderly_service.py
│   │   │── caregiver_service.py
│   │   │── caregiver_assignment_service.py
│   │
│   │── schemas/           # Pydantic schemas for data validation
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
│── frontend/
│   │── components/        # Streamlit UI components
│   │   │── __init__.py
│   │   │── add_data.py
│   │   │── manage_caregivers.py
│   │   │── manage_elderly.py
│   │   │── view_data.py
│   │
│   │── Dockerfile         # Frontend containerization
│   │── api_client.py      # Handles API communication
│   │── requirements.txt   # Frontend dependencies
│   │── ui.py              # Streamlit main UI file
│
│── docker-compose.yml     # Docker configuration for services
│── README.md              # Project documentation
│── pytest.ini             # Pytest configuration
```


## 💻 Technologies Used
- **FastAPI**: Backend framework.
- **PostgreSQL**: Database management.
- **Redis**: Caching layer for improved performance.
- **Docker**: Containerization.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation and settings management.
- **FPDF**: PDF generation.
- **pytest**: Testing framework.


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

**Frontend (Streamlit):**  
- **URL**: [http://localhost:8501](http://localhost:8501)  
  - Manage caregivers and their salaries, and generate a detailed PDF including all caregiver details and payment information."  
  - Manage elderly individuals, their tasks, and medications.  
  - View all data in a structured and user-friendly format.  

**Backend API (Swagger Documentation):**  
- **URL**: [http://localhost:8000/docs](http://localhost:8000/docs)  
  - Provides API documentation and allows you to test the backend endpoints directly.  


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


## 📬 Contact Info
**Ori Levi**  
📧 Email: Leviori1218@gmail.com  
🐙 GitHub: [OriLevi12](https://github.com/OriLevi12)

## illustration
![application design](frontend/media/ApplicationDesign.png)
