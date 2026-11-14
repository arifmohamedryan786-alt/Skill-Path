from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    user = None
    if token:
        try:
            payload = decode_access_token(token)
            if payload:
                user_id = payload.get("user_id")
                if user_id:
                    user = db.query(User).filter(User.id == user_id).first()
        except Exception:
            pass

    # Direct frictionless entry: if no token or token invalid, default to primary learner
    if not user:
        user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Default learner not seeded in database"
        )
    return user

def get_current_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    if current_user.role == "admin":
        return current_user
    # Direct access: provide seeded demo admin if learner visits admin portal
    admin_user = db.query(User).filter(User.role == "admin").first()
    if admin_user:
        return admin_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Administrator access required"
    )

