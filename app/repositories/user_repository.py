from sqlalchemy.orm import Session
from app.models.user import User
from typing import Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, username: str, email: str, password_hash: str) -> User:
        """Create user baru"""
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        
        return user
    
    def get_user_by_email(self, email:str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by id"""
        return self.db.query(User).filter(User.id == user_id).first()