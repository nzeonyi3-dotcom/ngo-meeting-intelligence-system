# Development Guide

## Local Development Setup

### Prerequisites

- Python 3.12+
- Node.js 18+ LTS
- PostgreSQL 16+ (optional, use Docker)
- Docker & Docker Compose (recommended)
- Git

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/nzeonyi3-dotcom/ngo-meeting-intelligence-system.git
   cd ngo-meeting-intelligence-system
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   ```

### Option 1: Docker Compose (Recommended)

```bash
docker compose up --build
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python3.12 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Set up database**
   ```bash
   # Create local PostgreSQL database
   createdb ngo_meeting_db
   ```

4. **Update .env**
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/ngo_meeting_db
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start dev server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Create .env.local**
   ```bash
   cp ../.env.example .env.local
   ```

3. **Start dev server**
   ```bash
   npm run dev
   ```

## Code Structure

### Backend Code Organization

```
backend/app/
├── main.py              # FastAPI app initialization
├── core/
│   ├── config.py        # Settings and configuration
│   ├── logging.py       # Logging setup
│   └── security.py      # Security utilities
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas (request/response)
├── repositories/        # Data access layer
├── services/            # Business logic
├── api/                 # API routes
│   └── v1/
│       ├── endpoints/   # Route handlers
│       └── deps.py      # Dependencies
└── middleware/          # Custom middleware
```

### Frontend Code Organization

```
frontend/
├── app/                 # Next.js App Router
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Home page
├── components/          # React components
├── lib/                 # Utilities
│   └── api.ts           # API client
├── types/               # TypeScript types
├── styles/              # CSS modules
└── public/              # Static files
```

## Development Workflow

### Adding a New Backend Endpoint

1. **Create schema** (`backend/app/schemas/`)
   ```python
   from pydantic import BaseModel
   
   class ItemSchema(BaseModel):
       name: str
       description: str | None = None
   ```

2. **Create model** (`backend/app/models/`)
   ```python
   from sqlalchemy import Column, Integer, String
   from app.models.base import Base
   
   class Item(Base):
       __tablename__ = "items"
       id = Column(Integer, primary_key=True)
       name = Column(String, nullable=False)
   ```

3. **Create migration**
   ```bash
   alembic revision --autogenerate -m "Add Item table"
   alembic upgrade head
   ```

4. **Create repository** (`backend/app/repositories/`)
   ```python
   from sqlalchemy.orm import Session
   from app.models import Item
   
   class ItemRepository:
       def __init__(self, db: Session):
           self.db = db
       
       def create(self, item: ItemSchema):
           db_item = Item(**item.dict())
           self.db.add(db_item)
           self.db.commit()
           return db_item
   ```

5. **Create service** (`backend/app/services/`)
   ```python
   from app.repositories import ItemRepository
   
   class ItemService:
       def __init__(self, repo: ItemRepository):
           self.repo = repo
       
       def create_item(self, item: ItemSchema):
           return self.repo.create(item)
   ```

6. **Create endpoint** (`backend/app/api/v1/endpoints/`)
   ```python
   from fastapi import APIRouter, Depends
   from app.api.deps import get_item_service
   from app.schemas import ItemSchema
   
   router = APIRouter()
   
   @router.post("/items", response_model=ItemSchema)
   async def create_item(
       item: ItemSchema,
       service: ItemService = Depends(get_item_service)
   ):
       return service.create_item(item)
   ```

### Adding a New Frontend Component

1. **Create component** (`frontend/components/`)
   ```typescript
   // components/MyComponent.tsx
   export default function MyComponent() {
     return <div>My Component</div>
   }
   ```

2. **Use in page**
   ```typescript
   // app/page.tsx
   import MyComponent from '@/components/MyComponent'
   
   export default function Home() {
     return (
       <main>
         <MyComponent />
       </main>
     )
   }
   ```

## Testing

### Backend Tests

1. **Write test** (`backend/tests/`)
   ```python
   import pytest
   from app.services import ItemService
   
   @pytest.mark.asyncio
   async def test_create_item():
       # Test implementation
       pass
   ```

2. **Run tests**
   ```bash
   cd backend
   pytest tests/ -v
   # With coverage
   pytest tests/ --cov=app --cov-report=html
   ```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Code Quality

### Backend Linting

```bash
cd backend

# Run pylint
pylint app/

# Run black (formatting)
black app/ tests/

# Run isort (import sorting)
isort app/ tests/

# Type checking with mypy
mypy app/
```

### Frontend Linting

```bash
cd frontend

# Run ESLint
npm run lint

# Fix issues
npm run lint -- --fix

# Format with Prettier
npm run format

# Type checking
npm run type-check
```

### Pre-commit Hooks (Optional)

Set up pre-commit hooks to run linters automatically:

```bash
pip install pre-commit
pre-commit install
```

## Database Migrations

### Create a Migration

```bash
cd backend
alembic revision --autogenerate -m "Descriptive message"
```

### Review Migration

Edit the generated file in `backend/migrations/versions/`

### Apply Migration

```bash
alembic upgrade head
```

### Revert Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic current
alembic history
```

## Environment Variables

### Development

Create `backend/.env` and `frontend/.env.local` with appropriate values:

```bash
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DEBUG=true
LOG_LEVEL=DEBUG

# Frontend
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Production

Set environment variables in deployment platform or CI/CD system. Never commit secrets.

## Docker Commands

```bash
# Build images
docker compose build

# Start services
docker compose up

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Remove volumes
docker compose down -v

# Access container shell
docker compose exec backend bash
docker compose exec frontend sh

# Run command in container
docker compose exec backend alembic upgrade head
```

## Debugging

### Backend Debugging

1. **Using print statements**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.debug(f"Variable: {variable}")
   ```

2. **Using debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

3. **VS Code debugging** - Add to `.vscode/launch.json`
   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Python: FastAPI",
         "type": "python",
         "request": "launch",
         "module": "uvicorn",
         "args": ["app.main:app", "--reload"],
         "jinja": true,
         "cwd": "${workspaceFolder}/backend"
       }
     ]
   }
   ```

### Frontend Debugging

1. **Browser DevTools** - Press F12
2. **VS Code debugging** - Install Debugger for Chrome extension
3. **React DevTools** - Browser extension for React component inspection

## Useful Commands

### Backend

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Start dev server with reload
uvicorn app.main:app --reload

# Start with specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run with multiple workers (production)
uvicorn app.main:app --workers 4
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Check for type errors
npm run type-check

# Lint and fix
npm run lint -- --fix
```

## Troubleshooting

### Backend won't start

1. Check Python version: `python --version`
2. Verify virtual environment is activated
3. Check DATABASE_URL is correct
4. Review logs for specific errors

### Frontend build fails

1. Delete node_modules: `rm -rf node_modules`
2. Clear npm cache: `npm cache clean --force`
3. Reinstall: `npm install`
4. Clear Next.js cache: `rm -rf .next`

### Port already in use

```bash
# Find process
lsof -i :8000
lsof -i :3000

# Kill process
kill -9 <PID>
```

### Database connection error

1. Verify PostgreSQL is running
2. Check DATABASE_URL format
3. Verify credentials
4. Check port 5432 is open

## Performance Optimization

### Backend
- Use database indexing for frequently queried fields
- Implement caching for static data
- Optimize N+1 queries with eager loading
- Use connection pooling

### Frontend
- Use React.memo for expensive components
- Implement code splitting with dynamic imports
- Optimize images with Next.js Image component
- Use CSS modules for scoped styling

## Security Best Practices

1. Never commit .env files
2. Rotate secrets regularly
3. Use HTTPS in production
4. Implement rate limiting
5. Add input validation
6. Use SQL parameterized queries (automatic with ORM)
7. Implement CSRF protection
8. Keep dependencies updated

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
