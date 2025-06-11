# User Registration API

A Flask-based REST API for user registration with data validation and SQLite persistence.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository and navigate to the project directory:
```bash
cd api-users
```

2. Build and start the containers:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:7000`

## API Documentation

Access the Swagger documentation at `http://localhost:7000/` for interactive API documentation.

## Available Endpoints

### 1. Create User
```bash
POST /users
```

Example request:
```bash
curl -X POST http://localhost:7000/users \
-H "Content-Type: application/json" \
-d '{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "(11) 98765-4321",
  "zip_code": "12345-678",
  "address": "Main Street",
  "number": "123",
  "city": "São Paulo",
  "state": "SP",
  "terms_accepted": true
}'
```

### 2. List Users
```bash
GET /users
```

Example request:
```bash
curl http://localhost:7000/users
```

## Data Validation Rules

- All fields are mandatory
- Email must be valid and unique
- Phone must follow Brazilian format: (XX) XXXXX-XXXX or (XX) XXXX-XXXX
- Zip code must follow Brazilian format: XXXXX-XXX
- State must be a valid Brazilian state abbreviation (2 letters)
- Terms must be accepted (true)

## Error Codes

- 400: Bad Request (validation errors)
- 409: Conflict (email already exists)
- 500: Internal Server Error

## Stopping the Application

To stop the application:
```bash
docker-compose down
```

## Data Persistence

The SQLite database is stored in the `./data` directory and persists between container restarts. 