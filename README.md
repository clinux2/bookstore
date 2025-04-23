# Web Bookstore Backend API

This is a Flask-based backend API for a web bookstore system. It uses MongoDB as the database and includes authentication for admin users.

## Features

- Admin registration and authentication
- JWT-based authentication
- CRUD operations for books
- MongoDB integration
- CORS support

## Prerequisites

- Python 3.7+
- MongoDB installed and running
- pip (Python package manager)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the MongoDB URI and secret key in `.env`

## Running the Application

1. Start MongoDB if it's not already running
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/register` - Register a new admin user
- `POST /api/login` - Login and get JWT token

### Books
- `GET /api/books` - Get all books
- `POST /api/books` - Add a new book (requires admin authentication)
- `PUT /api/books/<book_id>` - Update a book (requires admin authentication)
- `DELETE /api/books/<book_id>` - Delete a book (requires admin authentication)

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Example Requests

### Register Admin
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "yourpassword"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "yourpassword"}'
```

### Add Book
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-token>" \
  -d '{
    "title": "Book Title",
    "author": "Author Name",
    "price": 29.99,
    "description": "Book description",
    "stock": 100
  }'
``` 