# Media Service

Backend service for uploading, validating and managing video files built with FastAPI.

## Description
Media Service is a backend application that provides an API for uploading, validating and managing video files.

The application is built with FastAPI and uses PostgreSQL, SQLAlchemy ORM and automated testing.

## Features

- REST API for video management
- Upload and manage video files
- CRUD operations
- Video file validation using FFmpeg and libmagic
- Metadata extraction from video files
- PostgreSQL database integration

## Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### Database
- PostgreSQL
- SQLAlchemy
- Alembic

### Testing
- Pytest

### Media processing
- FFmpeg
- libmagic

### Tools
- Git

## Project Structure

```text
app/
├── api/
│   ├── core/
│   ├── routes/
│   ├── services/
│   └── utils/
├── data/
│   └── crud/
├── tests/
└── main.py
```

## How to run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start application

```bash
uvicorn app.main:app --reload
```

### API documentation

After starting the application:

```text
http://localhost:8000/docs
```

---

## Future Improvements

- Add Redis-based task queue for background video processing
- Add background workers for asynchronous processing
- Add frontend client
- Add Docker support
- Improve authentication system
