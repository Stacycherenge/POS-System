from sqlalchemy.orm import Session
from repositories.user import user_repository
from fastapi import HTTPException, status
from schemas.user import UserCreate, UserUpdate


def get_user(db: Session, id: int):
    user = user_repository.get(db, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return user


def list_users(db: Session):
    return user_repository.get_all(db)


def create_user(db: Session, data: UserCreate):
    user_data = data.model_dump()
    
    plain_password = user_data.pop("password")
    
    user_data["password_hash"] = plain_password + "_hashed" 
    
    return user_repository.create(db, user_data)


def update_user(db: Session, user_id: int, data: UserUpdate):
    user = get_user(db, user_id)
    
    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        plain_password = update_data.pop("password")
        update_data["password_hash"] = plain_password + "_hashed" 
        
    return user_repository.update(db, user, update_data)


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id) 
    return user_repository.delete(db, user)
