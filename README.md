
# Elder Care Management System

The Elder Care Management System is designed primarily for elderly individuals and their guardians, providing tools to manage caregivers, medications, and task lists. The system also generates a payment form detailing the caregiver's required salary, simplifying financial management for private care.

While the system is tailored for private use, it also includes functionality for managing elder care facilities, with the option for future expansions to enhance this capability.

---

## ✨ Features
1. 🛠️ Manage caregivers, elderly individuals, tasks, and medications.
2. 📝 Generate a PDF payment report for caregivers.
3. 🚀 Flexible and extensible design for future enhancements.

---

## 💻 Technologies Used
- **FastAPI**: Backend framework.
- **PostgreSQL**: Database management.
- **Docker**: Containerization.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation and settings management.
- **FPDF**: PDF generation.
- **pytest**: Testing framework.

---

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

---

### Step 3: Create a `.env` File
Create a `.env` file in the project's root directory and add the following variables:
```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=elder_care_db
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/elder_care_db
```

---

### Step 4: Build and Run the Application with Docker
```bash
docker-compose up --build
```

---

## 🛠️ Usage
### Access the API
Once the application is running, navigate to:
🔗 [http://localhost:8000/docs](http://localhost:8000/docs)

You can explore the API documentation and test endpoints directly from the interactive Swagger UI.

---

## 📬 Contact Info
**Ori Levi**  
📧 Email: Leviori1218@gmail.com  
🐙 GitHub: [OriLevi12](https://github.com/OriLevi12)
