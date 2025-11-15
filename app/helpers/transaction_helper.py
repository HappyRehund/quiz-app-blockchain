from functools import wraps
from sqlalchemy.orm import Session
from typing import Callable, Any


def transactional(func: Callable) -> Callable:
    """
    Decorator for adding transaction management to service methods.
    
    How it works:
    1. The method will be executed
    2. If successful -> auto commit
    3. If there is an error -> auto rollback
    
    Usage:
        @transactional
        def my_service_method(self, ...):
            # Your database operations here
            # Will be committed if no error
            # Will be rolled back if error occurs
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Cari db session dari instance (self.db)
        db: Session | None = None
        
        if len(args) > 0 and hasattr(args[0], 'db'):
            db = args[0].db
        
        if db is None:
            raise ValueError(
                f"No database session found in {func.__name__}. "
                "Ensure service class has 'db' attribute initialized in __init__"
            )
        
        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise e
    
    return wrapper


def read_only(func: Callable) -> Callable:
    """
    Decorator for read-only operations.
    This function do not commit, just for documentation that this method is read-only.
    
    Usage:
        @read_only
        def get_user(self, user_id: int):
            return self.user_repo.get_user_by_id(user_id)
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)
    
    return wrapper