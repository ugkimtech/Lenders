
# Loan Tracking System

A web-based loan tracking system built with Django to manage loans, payments, customers, and report.

## Features

- **Loan Management**: Create, view, update, and delete loans.
- **Customer Management**: Track borrower details and loan history.
- **Payment Tracking**: Record and monitor loan repayments.
- **User Authentication**: Secure login for admin, staff and customers.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript.
- **Database**: PostgreSQL, sqlite.
- 
## Installation

### Prerequisites
- Python 3.8+
- Pip (Python package manager)
- Virtualenv (recommended)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ugkimtech/Lenders.git
   cd Lenders
2. **setup virtual environment (optional)
   ```bash
   python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies
   ```bash
   pip install -r requirements.txt

4. **Configure database if want to use postgresql
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5. **Run migrations
   ```bash
   python manage.py migrate

6. **Create superuser
   ``bash
   python manage.py createsuperuser
7. **Run development server
   ```bash
   python manage.py runserver
8. **Access
   Use http://127.0.0.1:8000
   or http://localhost:8000

Author: KIMERA CHARLES
Version: 1.0.0
