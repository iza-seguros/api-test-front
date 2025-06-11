# User Registration API

A Flask-based REST API for user registration with data validation and SQLite persistence. This API provides a complete CRUD (Create, Read, Update, Delete) interface for managing user registrations with Brazilian-specific data validation.

## Features

- User registration with data validation
- Brazilian phone number and CEP (zip code) format validation
- Email uniqueness check
- SQLite database with persistent storage
- Swagger documentation
- Docker containerization
- Complete CRUD operations

## Prerequisites

- Docker
- Docker Compose
- Git (optional, for cloning the repository)

## Quick Start

1. Clone the repository (or download the files):
```bash
git clone <repository-url>
cd api-users
```

2. Build and start the containers:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:7000`

## API Documentation

Access the interactive Swagger documentation at `http://localhost:7000/` to:
- View all available endpoints
- Test the API directly from the browser
- See request/response schemas
- View validation rules

## API Endpoints

### 1. Create User
```bash
POST /users
```

Creates a new user with the provided information.

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

### 2. List All Users
```bash
GET /users
```

Retrieves a list of all registered users.

Example request:
```bash
curl http://localhost:7000/users
```

### 3. Get User by ID
```bash
GET /users/{id}
```

Retrieves a specific user by their ID.

Example request:
```bash
curl http://localhost:7000/users/1
```

### 4. Update User
```bash
PUT /users/{id}
```

Updates an existing user's information.

Example request:
```bash
curl -X PUT http://localhost:7000/users/1 \
-H "Content-Type: application/json" \
-d '{
  "full_name": "John Updated",
  "email": "john.updated@example.com",
  "phone": "(11) 98765-4321",
  "zip_code": "12345-678",
  "address": "New Street",
  "number": "456",
  "city": "Rio de Janeiro",
  "state": "RJ",
  "terms_accepted": true
}'
```

### 5. Delete User
```bash
DELETE /users/{id}
```

Removes a user from the system.

Example request:
```bash
curl -X DELETE http://localhost:7000/users/1
```

## Data Validation Rules

All endpoints enforce the following validation rules:

- **Required Fields**: All fields are mandatory
- **Email**:
  - Must be a valid email format
  - Must be unique in the system
- **Phone**: Must follow Brazilian format
  - (XX) XXXXX-XXXX (mobile)
  - (XX) XXXX-XXXX (landline)
- **Zip Code (CEP)**: Must follow Brazilian format
  - XXXXX-XXX
- **State**: Must be a valid Brazilian state abbreviation (2 letters)
  - Valid states: AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO
- **Terms**: Must be accepted (true)

## Response Codes

- **200**: Success (GET, PUT)
- **201**: Created (POST)
- **204**: No Content (DELETE)
- **400**: Bad Request (validation errors)
- **404**: Not Found (user not found)
- **409**: Conflict (email already exists)
- **500**: Internal Server Error

## Development

### Project Structure
```
api-users/
├── app/
│   ├── app.py
│   └── requirements.txt
├── data/
│   └── users.db
├── docker-compose.yml
├── Dockerfile
└── README.md
```

### Running in Development Mode

1. Start the application:
```bash
docker-compose up --build
```

2. Stop the application:
```bash
docker-compose down
```

3. View logs:
```bash
docker-compose logs -f
```

### Data Persistence

- The SQLite database is stored in the `./data` directory
- Data persists between container restarts
- The database file is mounted as a Docker volume

## Error Handling

The API provides detailed error messages for various scenarios:

- Missing required fields
- Invalid data formats
- Duplicate email addresses
- Non-existent users
- Server errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 