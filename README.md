# Django REST API - Platform Service

A comprehensive RESTful API built with Django and Django REST Framework, designed to power multi-service platforms. This project demonstrates production-ready Django development patterns including authentication, dashboard analytics, transaction management, and reporting capabilities.

## Overview

This is a full-featured backend API that handles core platform functionality. It serves as the backbone for a SaaS platform with user management, real-time analytics, transaction processing, and report generation. Perfect for learning Django best practices or as a foundation for your next project.

### Key Highlights
- **JWT Authentication** - Secure token-based authentication
- **Multi-app Architecture** - Modular, scalable design
- **Real-time Metrics** - Dashboard analytics with daily stats
- **Transaction Management** - Full CRUD with status tracking
- **Report Generation** - Date-range reports with JSON storage
- **PostgreSQL Database** - Production-ready relational database
- **CORS Enabled** - Seamless frontend integration
- **Comprehensive Documentation** - Clear API endpoints and examples

## Tech Stack

**Backend:**
- Django 4.x - Web framework
- Django REST Framework - API development
- Django REST Framework SimpleJWT - JWT authentication
- PostgreSQL - Database
- Gunicorn - WSGI server
- WhiteNoise - Static files serving

**Development:**
- Python 3.11+
- pip - Package manager
- Virtual Environment - Isolation

**Deployment:**
- Render.com - Hosting platform

## Prerequisites

Before you begin, ensure you have:
- Python 3.11 or higher
- pip (Python package manager)
- PostgreSQL (for production)
- Git
- Postman or similar API testing tool (optional)
- Virtual environment knowledge

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/django-rest-api.git
cd django-rest-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
FRONTEND_URL=http://localhost:3000
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

Generate a SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

Access the admin panel at `http://localhost:8000/admin/`

## Project Structure

```
django-rest-api/
├── config/                 # Project settings and URLs
│   ├── settings.py        # Main Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
│
├── accounts/              # User authentication and profiles
│   ├── models.py          # UserProfile model
│   ├── serializers.py     # User serializers
│   ├── views.py           # Auth viewsets
│   ├── urls.py            # Auth URLs
│   └── admin.py           # Admin configuration
│
├── dashboard/             # Analytics and metrics
│   ├── models.py          # DashboardMetric model
│   ├── serializers.py     # Dashboard serializers
│   ├── views.py           # Dashboard viewsets
│   └── admin.py           # Admin configuration
│
├── transactions/          # Transaction management
│   ├── models.py          # Transaction model
│   ├── serializers.py     # Transaction serializers
│   ├── views.py           # Transaction viewsets
│   └── admin.py           # Admin configuration
│
├── reports/               # Report generation
│   ├── models.py          # Report model
│   ├── serializers.py     # Report serializers
│   ├── views.py           # Report viewsets
│   └── admin.py           # Admin configuration
│
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore rules
├── build.sh               # Production build script
├── runtime.txt            # Python runtime version
└── README.md              # This file
```

## API Endpoints

### Authentication

**Obtain JWT Token**
```
POST /api/auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Refresh Token**
```
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

### Users & Profiles

**Register New User**
```
POST /api/users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Get Current User Profile**
```
GET /api/profiles/me/
Authorization: Bearer <access_token>
```

**Update User Profile**
```
PUT /api/profiles/me/update_profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "phone": "1234567890",
  "avatar": "https://example.com/avatar.jpg"
}
```

### Dashboard

**Get Dashboard Summary**
```
GET /api/dashboard/metrics/summary/
Authorization: Bearer <access_token>

Response:
{
  "total_revenue": 5000.00,
  "total_transactions": 25,
  "completed_transactions": 20,
  "pending_transactions": 3,
  "failed_transactions": 2,
  "last_30_days_revenue": 2500.00
}
```

**Get 7-Day Statistics**
```
GET /api/dashboard/metrics/stats/
Authorization: Bearer <access_token>

Response:
{
  "daily_stats": [
    {
      "date": "2024-01-25",
      "revenue": 500.00,
      "transactions": 5
    },
    ...
  ]
}
```

### Transactions

**List Transactions**
```
GET /api/transactions/
Authorization: Bearer <access_token>

Query Parameters:
- status=completed (filter by status)
- search=description (search in description/transaction_id)
- ordering=-created_at (sort by field)
```

**Create Transaction**
```
POST /api/transactions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "amount": 100.00,
  "currency": "USD",
  "type": "purchase",
  "status": "pending",
  "description": "Payment for order",
  "payment_method": "credit_card"
}
```

**Get Transaction Details**
```
GET /api/transactions/{id}/
Authorization: Bearer <access_token>
```

**Update Transaction Status**
```
PATCH /api/transactions/{id}/update_status/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "completed"
}
```

Valid statuses: `pending`, `completed`, `failed`, `refunded`

**Get Transactions by Status**
```
GET /api/transactions/by_status/?status=completed
Authorization: Bearer <access_token>
```

### Reports

**List Reports**
```
GET /api/reports/
Authorization: Bearer <access_token>
```

**Generate Revenue Report**
```
POST /api/reports/generate_revenue_report/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}

Response:
{
  "id": 1,
  "title": "Revenue Report 2024-01-01 to 2024-01-31",
  "report_type": "revenue",
  "data": {
    "total_revenue": 5000.00,
    "transaction_count": 25,
    "by_type": {
      "purchase": 20,
      "refund": 5
    }
  },
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "generated_at": "2024-01-25T10:30:00Z"
}
```

## Authentication

This API uses JWT (JSON Web Token) authentication. All protected endpoints require:

```
Authorization: Bearer <your_access_token>
```

**Token Lifespan:**
- Access Token: 1 hour
- Refresh Token: 7 days

## Deployment

### Deploy to Render

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

2. **Create Render Account** and connect your GitHub

3. **Create Web Service**
   - Runtime: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

4. **Add Environment Variables**
```
DEBUG=False
SECRET_KEY=<generated-key>
ALLOWED_HOSTS=your-app.onrender.com
DB_NAME=<database_name>
DB_USER=<database_user>
DB_PASSWORD=<database_password>
DB_HOST=<database_host>
DB_PORT=5432
FRONTEND_URL=https://your-frontend.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

5. **Create PostgreSQL Database** (optional)
   - Create a PostgreSQL service on Render
   - Link it to your web service

6. **Deploy** - Render auto-deploys on push

## Testing with Postman

1. **Import Collection**
   - Create a new collection in Postman
   - Add requests for each endpoint

2. **Set Environment Variables**
```json
{
  "baseUrl": "http://localhost:8000/api",
  "access_token": "",
  "username": "john_doe",
  "password": "password123"
}
```

3. **Get Access Token**
   - POST to `/auth/login/`
   - In Tests tab: `pm.environment.set("access_token", pm.response.json().access);`
   - Use `{{access_token}}` in Authorization headers

## Database Connection (pgAdmin)

To connect locally:

1. Open pgAdmin 4
2. Register new server
3. Connection settings:
   - Hostname: Your Render database hostname
   - Port: 5432
   - Database: Your database name
   - Username: Your database user
   - Password: Your database password
   - SSL mode: Require

## Key Django Concepts

**ViewSets** - Auto-generate CRUD endpoints for models

**Serializers** - Validate and transform data (like validation schemas)

**Permissions** - Control who can access endpoints

**Models** - Define database structure

**Middleware** - Process requests/responses globally

## Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Render Deployment Guide](https://render.com/docs)

## Contributing

Contributions are welcome! 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Built as a learning project and production-ready starter template.

## Support

For issues, questions, or suggestions:
- Open an GitHub issue
- Check existing documentation
- Review API endpoint examples

---
