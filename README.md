# TaskFlow Backend

A modern FastAPI-based backend for task management and scheduling. TaskFlow provides a comprehensive REST API for managing tasks, events, appointments, and user authentication with JWT-based security.

## Features

- **User Management**: Create accounts, manage user profiles with secure password hashing using Argon2
- **Task Management**: Create, update, and delete tasks with support for:
  - Priority levels
  - Due dates and deadlines
  - Task completion status
  - Recurring tasks with customizable recurrence intervals
  - Detailed descriptions
- **Event Management**: Schedule and manage events
- **Appointment Management**: Track and manage appointments
- **Authentication**: JWT-based token authentication with secure token generation and validation
- **Database**: SQLite database with SQLAlchemy ORM for data persistence

## Tech Stack

- **Framework**: FastAPI 0.121.0
- **Server**: Uvicorn 0.38.0
- **Database**: SQLite with SQLAlchemy 2.0.44
- **Authentication**: JWT (PyJWT 2.8.0), OAuth2, Argon2
- **Data Validation**: Pydantic 2.12.4
- **Environment Management**: Python-dotenv 1.2.1
- **Monitoring**: Sentry SDK 2.43.0

## Project Structure

```
taskflow-backend/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── appointments.py     # Appointment endpoints
│   │   ├── events.py           # Event endpoints
│   │   ├── tasks.py            # Task endpoints
│   │   └── users.py            # User endpoints
│   ├── core/                   # Core functionality
│   │   ├── auth.py             # Authentication logic
│   │   └── utils/
│   │       └── helpers.py      # Utility functions
│   ├── db/
│   │   └── schema.py           # Database schema and connection
│   ├── models/                 # Data models
│   │   ├── appointments.py     # Appointment model
│   │   ├── events.py           # Event model
│   │   ├── tasks.py            # Task model
│   │   └── users.py            # User model
│   ├── services/               # Business logic services
│   ├── main.py                 # FastAPI application entry point
│   └── __init__.py
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd taskflow-backend
```

2. **Create a virtual environment** (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root directory:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./taskflow.db
```

**Important**: The `SECRET_KEY` environment variable is required for JWT token generation. If not set, the application will raise an error.

## Usage

### Running the Server

Start the development server with:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/token` - Generate JWT access token
- `GET /auth/me` - Get current user information

### Users
- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user information
- `DELETE /users/{user_id}` - Delete user account

### Tasks
- `GET /tasks/` - List all tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/{task_id}` - Get task details
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### Events
- `GET /events/` - List all events
- `POST /events/` - Create a new event
- `GET /events/{event_id}` - Get event details
- `PUT /events/{event_id}` - Update an event
- `DELETE /events/{event_id}` - Delete an event

### Appointments
- `GET /appointments/` - List all appointments
- `POST /appointments/` - Create a new appointment
- `GET /appointments/{appointment_id}` - Get appointment details
- `PUT /appointments/{appointment_id}` - Update an appointment
- `DELETE /appointments/{appointment_id}` - Delete an appointment

## Authentication

TaskFlow uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. **Get a Token**
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=yourpassword"
```

2. **Use the Token**
Include the token in the Authorization header for subsequent requests:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  "http://localhost:8000/tasks/"
```

## Database

The application uses SQLite for data persistence. The database file (`taskflow.db`) is automatically created in the project root on first run.

### Database Schema

The database includes the following main tables:
- **users**: User accounts and authentication credentials
- **tasks**: Task records with status and recurrence information
- **events**: Event scheduling data
- **appointments**: Appointment records

## Configuration

Key configurations are managed through environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Secret key for JWT token signing | Yes |
| `DATABASE_URL` | SQLite database path (default: `sqlite:///./taskflow.db`) | No |

## Development

### Project Standards
- **Code Style**: Follow PEP 8 guidelines
- **Type Hints**: Use Python type hints for better IDE support
- **Docstrings**: Document functions and classes with docstrings

### Adding New Features

1. Create models in `app/models/`
2. Add database schema in `app/db/schema.py`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/api/`
5. Include proper error handling and validation

## Error Handling

The API follows standard HTTP status codes:
- `200 OK` - Successful request
- `201 Created` - Resource successfully created
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or failed
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Security

- **Password Hashing**: Passwords are hashed using Argon2 for secure storage
- **JWT Tokens**: Secure token-based authentication with configurable expiration
- **OAuth2**: Standard OAuth2 password flow for token generation
- **CORS**: Configure CORS as needed for your frontend

## Monitoring

The application integrates with Sentry SDK for error tracking and monitoring. Configure Sentry DSN in your `.env` for production deployments.

## Contributing

When contributing to this project:
1. Create a feature branch
2. Make your changes
3. Ensure all endpoints are properly documented
4. Test your changes thoroughly
5. Submit a pull request with a clear description

## License

[Add your license information here]

## Support

For issues and questions:
- Open an issue on the repository
- Contact the development team
- Check existing documentation

## Future Enhancements

- [ ] Email notifications for due tasks
- [ ] Task categories and tags
- [ ] Task collaboration and sharing
- [ ] Advanced filtering and search
- [ ] Rate limiting
- [ ] API versioning
- [ ] Comprehensive test suite
- [ ] Deployment guides (Docker, Heroku, etc.)
