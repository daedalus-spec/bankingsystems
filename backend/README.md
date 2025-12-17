#  Bank Backend API

A comprehensive banking dashboard backend built with FastAPI, SQLAlchemy, and PostgreSQL/SQLite.

## Features

- 🔐 **JWT Authentication** - Secure user authentication with token-based system
- 👤 **User Management** - Registration, login, and profile management
- 💰 **Account Management** - Multiple account types (checking, savings)
- 💳 **Card Management** - Debit and credit card tracking
- 📊 **Transactions** - Track income and expenses with categories
- 🧾 **Bill Management** - Schedule and pay recurring bills
- 📈 **Analytics** - Income vs outcome charts and financial insights
- 🔄 **RESTful API** - Clean, well-documented API endpoints

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL/SQLite** - Relational database
- **Pydantic** - Data validation using Python type annotations
- **JWT** - JSON Web Tokens for authentication
- **Bcrypt** - Password hashing

## Project Structure

```
backend/
├── main.py              # FastAPI application and endpoints
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── database.py          # Database configuration
├── seed_data.py         # Script to populate test data
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md           # This file
```

## Installation

### 1. Clone and Setup

```bash
# Create project directory
mkdir bank-backend
cd bank-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file with your configuration (or use the provided template).

### 4. Initialize Database

```bash
# Run the seed script to create tables and add test data
python seed_data.py
```

### 5. Start the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /token` - Login and get access token

### User
- `GET /users/me` - Get current user profile
- `GET /dashboard` - Get complete dashboard data

### Accounts
- `GET /accounts` - List all user accounts
- `POST /accounts` - Create new account

### Transactions
- `GET /transactions` - List transactions (paginated)
- `POST /transactions` - Create new transaction

### Cards
- `GET /cards` - List all user cards
- `POST /cards` - Add new card

### Bills
- `GET /bills` - List all bills
- `POST /bills` - Create new bill
- `PUT /bills/{bill_id}/pay` - Pay a bill

### Analytics
- `GET /analytics/income-outcome` - Get income vs outcome data

## Authentication Flow

1. **Register**: POST to `/register` with email, full_name, and password
2. **Login**: POST to `/token` with email (as username) and password
3. **Get Token**: Receive access_token in response
4. **Use Token**: Add `Authorization: Bearer {access_token}` header to all requests

## Example Usage

### Register User
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "securepassword123"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

### Get Dashboard (with token)
```bash
curl -X GET "http://localhost:8000/dashboard" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create Transaction
```bash
curl -X POST "http://localhost:8000/transactions" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": 1,
    "amount": 100.00,
    "transaction_type": "credit",
    "category": "income",
    "description": "Salary payment",
    "recipient_name": "Company XYZ"
  }'
```

## Database Setup

### SQLite (Default - No Setup Required)
The default configuration uses SQLite, which creates a `banking.db` file automatically.

### PostgreSQL (Recommended for Production)

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE banking_db;
CREATE USER banking_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE banking_db TO banking_user;
```

3. Update `database.py`:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://banking_user:your_password@localhost/banking_db"
```

### MySQL

1. Install MySQL
2. Create database:
```sql
CREATE DATABASE banking_db;
CREATE USER 'banking_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON banking_db.* TO 'banking_user'@'localhost';
```

3. Update `database.py`:
```python
SQLALCHEMY_DATABASE_URL = "mysql://banking_user:your_password@localhost/banking_db"
```

## Test Credentials

After running `seed_data.py`:
- **Email**: ahsan.jilani@dacatibank.com
- **Password**: password123

## Security Notes

1. **Change SECRET_KEY**: Generate a secure key:
```bash
openssl rand -hex 32
```

2. **Use HTTPS**: Always use HTTPS in production
3. **Environment Variables**: Never commit `.env` file
4. **Password Policy**: Implement strong password requirements
5. **Rate Limiting**: Add rate limiting for production

## Frontend Integration

Add CORS middleware (already configured in main.py):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t dacati-bank-api .
docker run -p 8000:8000 dacati-bank-api
```

### Using Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku main
```

## Troubleshooting

### Issue: Module not found
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Database connection error
- Check DATABASE_URL in .env
- Ensure database server is running
- Verify credentials

### Issue: CORS error
- Check ALLOWED_ORIGINS in .env
- Ensure frontend URL is whitelisted

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - Feel free to use this project for learning and commercial purposes.

## Support

For issues and questions:
- Open an issue on GitHub
- Check API documentation at `/docs`
- Review error messages in terminal

## Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Email notifications for transactions
- [ ] Automated bill payments
- [ ] Investment tracking
- [ ] Budget planning features
- [ ] Multi-currency support
- [ ] Mobile app API optimizations
- [ ] Webhooks for external integrations