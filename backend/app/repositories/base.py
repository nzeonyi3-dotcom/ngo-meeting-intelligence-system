"""Base repository with common CRUD operations."""

from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, and_
from typing import TypeVar, Generic, List, Optional, Dict, Any
from app.database.base import Base

T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, db: Session, model: type[T]):
        self.db = db
        self.model = model
    
    def create(self, obj_in: Dict[str, Any]) -> T:
        """Create a new object."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, id: Any) -> Optional[T]:
        """Get object by ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all objects with pagination."""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: Any, obj_in: Dict[str, Any]) -> Optional[T]:
        """Update an object."""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            if value is not None and hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: Any) -> bool:
        """Delete an object."""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    def soft_delete(self, id: Any) -> Optional[T]:
        """Soft delete (mark as inactive)."""
        return self.update(id, {"is_active": False})
