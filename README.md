# 💰 DRF Expense Tracker API

A production-ready REST API for personal financial management, built with **Django REST Framework**. 
This project demonstrates modern backend practices including JWT authentication, data isolation, bulk operations, analytics, and interactive documentation.

## 🚀 Features

### 🔐 Authentication & Security
- **JWT Authentication**: Secure stateless auth using `simplejwt` (Login, Register, Refresh).
- **Throttling**: Rate limiting enabled to block brute-force attacks (User, Anon, and Scoped limits).
- **Role-Based Access Control (RBAC)**:
    - **Manager**: Read-only global access.
    - **Admin**: Full control including deletion.
    - **User**: Private access to own data only.
- **Data Isolation**: Row-level security powered by custom Mixins.
- **User Profile**: Self-service profile management.

### 💸 Core Functionality
- **Expenses & Income**: Full CRUD operations.
- **Categorization**: System validates category types (Income vs Expense).
- **Evidence**: File/Image upload support for transactions.
- **Advanced Filtering**: Filter by date, category, amount, etc.

### 📊 Dashboard & Analytics
- **Financial Summary**: Real-time Total Income, Expense, and Net Profit.
- **Chart Data**: Aggaggregated spending/income by category (perfect for Pie/Bar charts).
- **Trends**: Month-over-month filtering.

### 🔔 Notifications
- **Event-Driven**: Automatically generates notifications when important actions occur (e.g., New Expense).
- **Architecture**: Powered by **Django Signals** (Decoupled logic).
- **In-App**: Unread badge counts and history list.

### 🔄 Data Management
- **Bulk Import**: Upload CSV files to create multiple expenses instantly.
- **Smart Mapping**: Automatically maps CSV categories by Name or ID.
- **Export**: Download transaction history.

### 📚 Documentation
- **Swagger UI**: Interactive API testing interface via `drf-spectacular`.
- **ReDoc**: Clean, organized API reference.

---

## 🛠️ Technology Stack

- **Framework**: Django 5 + Django REST Framework (DRF)
- **Database**: PostgreSQL (Ready)
- **Auth**: `djangorestframework-simplejwt`
- **Docs**: `drf-spectacular` (OpenAPI 3.0)
- **Utilities**: `django-filter`, `rest_framework_csv`

---

## ⚡ Getting Started

### 1. Clone & Setup
```bash
git clone https://github.com/wasiimakram/drf_expense_tracker.git
cd drf_expense_tracker

# Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Run Server
```bash
python manage.py runserver
```

---

## 📖 API Documentation

Once the server is running, explore the APIs at:
- **Swagger UI**: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
- **ReDoc**: [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

---

## 🧪 Testing

```bash
# Run Unit Tests (Coming Soon)
python manage.py test
```
