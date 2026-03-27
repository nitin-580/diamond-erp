# 💎 Diamond ERP Backend

A production-grade, asynchronous ERP system built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy** to manage diamond processing workflows, worker assignments, and automated performance incentives.

---

## 🚀 Key Modules

### 🔹 **1. Diamond Lifecycle Management**
*   **Track Processing Stages**: Procurement → Planning → Laser Cutting → Polishing → Grading → Inventory → Sold.
*   **Real-time Status**: Live monitoring of "time spent" in each stage to identify production bottlenecks.
*   **Sequence Validation**: Automated detection of "skipped" processes with audit logging.

### 🔹 **2. Worker Performance & Incentives**
*   **Task Assignment**: Assign diamonds to workers for specific production processes.
*   **Automated Incentives**: Credits ₹100 reward automatically when a diamond reaches the `completed` stage.
*   **Financial Insights**: Monthly earnings breakdowns and total performance reports for workers.

### 🔹 **3. Process Automation**
*   **Custom Definitions**: Admin-defined processes with `expected_duration` for SLA compliance.
*   **Delay Monitoring**: Automated flags for diamonds showing signs of delay.
*   **Process History**: Comprehensive logs (`from_stage` to `to_stage`) with custom descriptions.

### 🔹 **4. Security & Authentication**
*   **JWT Security**: Role-based access control (Admin, Manager, Worker).
*   **Data Integrity**: Workers can only access their specific assignments and personal earnings.

---

## 🏗️ Technical Architecture

*   **Core Framework**: FastAPI (High-performance API)
*   **Database**: PostgreSQL with SQLAlchemy ORM
*   **Authentication**: JWT (JSON Web Tokens) with `passlib` & `bcrypt`
*   **Testing**: `pytest` for full integration coverage across 30+ endpoints
*   **Analytics**: Structured dashboard endpoints for throughput and worker load monitoring

---

## ⚙️ Project Structure

```text
apps/api/app/
├── api/v1/endpoints/  # Route controllers (Diamond, Worker, Incentive, Auth)
├── models/            # SQLAlchemy database schemas
├── repositories/      # Data access layer (Separation of Concerns)
├── services/          # Pure business logic layer
├── schemas/           # Pydantic request/response models
└── db/                # Database session and connectivity
```

---

## 🛠️ Quick Start

### 1. Prerequisites
*   Python 3.11+
*   PostgreSQL 14+

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/nitin-580/diamond-erp.git
cd diamond-erp

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
# Set PYTHONPATH to apps/api
export PYTHONPATH=$PYTHONPATH:$(pwd)/apps/api
python3 apps/api/init_db_run.py
python3 apps/api/seed_processes.py
```

### 4. Run Server
```bash
cd apps/api
python3 -m uvicorn app.main:app --port 8001 --reload
```

---

## 🧪 Testing

To run the full integration suite covering all modules:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/apps/api
pytest apps/api/test_integration.py -v
```

---

## 📄 API Documentation
Once running, explore interactive docs at:
*   **Swagger API**: `http://localhost:8001/docs`
*   **Redoc**: `http://localhost:8001/redoc`

---
*Maintained by Nitinkumar (High Performance Diamond ERP)*
