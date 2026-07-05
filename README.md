# NGO Meeting Intelligence System

A production-ready monorepo for the NGO Meeting Intelligence System, featuring a modern Next.js frontend and a FastAPI backend with PostgreSQL database.

## Project Structure

```
ngo-meeting-intelligence-system/
├── frontend/                 # Next.js application
├── backend/                  # FastAPI application
├── infrastructure/           # Docker and deployment configs
├── docs/                     # Documentation
├── docker-compose.yml        # Multi-container orchestration
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Tech Stack

### Frontend
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Code Quality**: ESLint, Prettier
- **Node Version**: 18+ LTS

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.12
- **Database ORM**: SQLAlchemy 2.x
- **Migrations**: Alembic
- **Configuration**: Pydantic Settings
- **Server**: Uvicorn
- **Logging**: Structured logging

### Infrastructure
- **Database**: PostgreSQL 16
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Prerequisites

- Docker & Docker Compose 2.20+
- Python 3.12+ (for local development)
- Node.js 18+ LTS (for local development)
- PostgreSQL 16 (optional, use Docker Compose instead)

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/nzeonyi3-dotcom/ngo-meeting-intelligence-system.git
   cd ngo-meeting-intelligence-system
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start all services**
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development Setup

#### Backend Setup

1. **Create and activate virtual environment**
   ```bash
   cd backend
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp ../.env.example .env
   # Edit .env with your local database URL
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables**
   ```bash
   cp ../.env.example .env.local
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

## Environment Variables

See `.env.example` for all available environment variables. Key configurations:

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Backend API endpoint
- `NEXT_PUBLIC_APP_NAME`: Application display name
- `NEXT_PUBLIC_APP_VERSION`: Application version

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (change in production)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `CORS_ORIGINS`: Allowed CORS origins

## API Endpoints

### Health Check
- `GET /health` - Health status
  ```json
  {"status": "ok"}
  ```

### Application Info
- `GET /api/v1/info` - Application information
  ```json
  {
    "name": "NGO Meeting Intelligence System",
    "version": "1.0.0",
    "status": "ok"
  }
  ```

## Development Workflow

### Code Quality

**Backend**
```bash
cd backend
pip install -r requirements-dev.txt
# Linting
pylint app/
# Type checking
mypy app/
# Testing
pytest tests/
# Format code
black app/ tests/
```

**Frontend**
```bash
cd frontend
# Linting
npm run lint
# Type checking
npm run type-check
# Testing
npm run test
# Format code
npm run format
```

### Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Revert last migration:
```bash
alembic downgrade -1
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Docker Commands

```bash
# Build and start all services
docker compose up --build

# Run services in background
docker compose up -d --build

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f backend
docker compose logs -f frontend

# Stop all services
docker compose down

# Remove all data (including volumes)
docker compose down -v

# Run backend migrations
docker compose exec backend alembic upgrade head

# Access backend container shell
docker compose exec backend bash

# Access frontend container shell
docker compose exec frontend sh
```

## Troubleshooting

### Database Connection Issues

**Issue**: Backend cannot connect to PostgreSQL

**Solution**:
1. Ensure PostgreSQL container is running: `docker compose ps`
2. Check DATABASE_URL in .env file
3. Verify port 5432 is not in use
4. Restart services: `docker compose down && docker compose up --build`

### Port Already in Use

**Issue**: Port 3000 or 8000 is already in use

**Solution**:
```bash
# Find process using port 3000
lsof -i :3000
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

### Module Not Found Errors (Backend)

**Issue**: Python module import errors in Docker

**Solution**:
1. Rebuild containers: `docker compose up --build`
2. Check requirements.txt is up to date
3. Verify PYTHONPATH is set correctly in Dockerfile

### Next.js Build Errors

**Issue**: Frontend build fails in Docker

**Solution**:
1. Clear .next folder: `rm -rf frontend/.next`
2. Rebuild: `docker compose up --build`
3. Check Node version matches requirements

### Health Check Fails

**Issue**: `/health` endpoint returns error

**Solution**:
1. Check backend logs: `docker compose logs backend`
2. Verify DATABASE_URL is correct
3. Run migrations: `docker compose exec backend alembic upgrade head`
4. Restart backend: `docker compose restart backend`

## CI/CD Pipeline

GitHub Actions workflow runs on every push and pull request:
- Installs dependencies (backend and frontend)
- Runs linting checks (backend and frontend)
- Verifies builds (backend and frontend)
- Runs tests (if configured)

See `.github/workflows/ci.yml` for workflow configuration.

## Production Deployment

### Pre-deployment Checklist
- [ ] Update `SECRET_KEY` with a strong random value
- [ ] Set `DEBUG=false`
- [ ] Update `CORS_ORIGINS` with production domain
- [ ] Update database credentials
- [ ] Run all migrations
- [ ] Test health endpoint
- [ ] Review environment variables

### Deployment Options

1. **Docker Compose on VPS**
   - Build and push images to registry
   - Update docker-compose.yml for production
   - Use environment-specific .env files

2. **Kubernetes**
   - Create Kubernetes manifests from Dockerfile configurations
   - Use ConfigMaps and Secrets for environment variables
   - Set up ingress for frontend and backend

3. **Cloud Platforms**
   - Vercel: Deploy frontend
   - Railway/Render: Deploy backend
   - AWS RDS: Managed PostgreSQL

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Add your feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create a GitHub Issue
- Check existing issues for solutions
- Review documentation in `/docs` folder

## Architecture Overview

### Clean Architecture Principles

The project follows clean architecture patterns:

**Backend**:
- `models/` - Database models (Entities)
- `schemas/` - Pydantic models (DTOs)
- `repositories/` - Data access layer
- `services/` - Business logic layer
- `api/` - HTTP handlers
- `core/` - Configuration and utilities

**Frontend**:
- `app/` - Page components and routes
- `components/` - Reusable UI components
- `lib/` - Utilities and helpers
- `hooks/` - Custom React hooks
- `types/` - TypeScript interfaces

### Dependency Injection

**Backend**: FastAPI dependency injection via `Depends()`

**Frontend**: Custom hooks and context providers

## Monitoring and Logging

### Backend Logging
- Structured JSON logging with configurable levels
- Request/response logging middleware
- Database query logging (in debug mode)

### Frontend Logging
- Console logging with development/production separation
- Error boundary integration
- Performance monitoring ready

## Security Considerations

- CORS configured to specific origins
- Environment variables for sensitive data
- SQL injection prevention via SQLAlchemy ORM
- XSS protection via Next.js built-in features
- CSRF tokens (implement in future)
- Rate limiting (implement in future)
- Authentication (implement in future)

## Performance Optimization

### Backend
- Connection pooling (SQLAlchemy)
- Async/await support ready
- Query optimization via ORM

### Frontend
- Image optimization via Next.js Image component
- Code splitting and lazy loading
- CSS optimization with Tailwind

## Version History

### v1.0.0 (Initial Release)
- Next.js frontend with landing page
- FastAPI backend with health checks
- PostgreSQL database integration
- Docker & Docker Compose setup
- GitHub Actions CI/CD pipeline
- Comprehensive documentation
