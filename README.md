
# Cloud Billing & Access API

A small backend project developed to practice cloud engineering concepts, including REST APIs, authentication, role-based access control, database operations, automated testing, and container orchestration.

Built with Python and FastAPI.

## Technologies

- Python 3.14
- FastAPI and Uvicorn
- SQLite
- Pytest
- Docker
- Kubernetes (kind)
- GitHub Actions (workflow configured)

## Features

- Bearer token authentication
- Role-based access control (RBAC)
- Retrieve the authenticated user's information
- Retrieve user information by ID
- Delete users with permission checks
- SQLite data persistence
- Automated API tests

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Health check |
| GET | /users/me | Current user information |
| GET | /users/{user_id} | Retrieve a user |
| DELETE | /users/{user_id} | Delete a user |

## Local Setup

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Initialize the SQLite database:

```bash
python app/database.py
```

Start the API:

```bash
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to explore the API.

## Testing

Run the API tests:

```bash
python -m pytest -v tests/test_user.py
```

The test suite covers authentication, access control, user retrieval, and deletion.

A temporary SQLite database is used for the deletion test to avoid modifying development data.

## Docker and Kubernetes

The project includes a Dockerfile and Kubernetes Deployment and Service manifests.

The FastAPI health endpoint has been tested locally using Docker and a three-replica Kubernetes Deployment with kind.

The current container configuration does not initialize a shared user database.

## CI/CD

A GitHub Actions workflow is configured to install dependencies, initialize SQLite, and run pytest.

The remote workflow has not been validated because GitHub Actions execution was blocked by an account billing restriction.

## Current Limitations

This project is an educational prototype, not a production-ready service.

- Authentication uses hard-coded demonstration tokens.
- Tokens are stored in process memory.
- SQLite is suitable for local development but is not configured as shared storage between Kubernetes Pods.
- The current container deployment has only been verified through the health endpoint.
- A production deployment would require shared persistent storage, secure credential management, and stronger authentication.

## Future Improvements

- Replace SQLite with shared PostgreSQL.
- Implement persistent authentication and token revocation.
- Add integration tests for containerized deployments.
- Improve database configuration and error handling.
- Validate the complete CI/CD pipeline.
