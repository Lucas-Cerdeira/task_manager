from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


class UserDbServices():

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        try:
            user_dict = dict(user)
            new_user = User(**user_dict)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as erro:
            raise erro
        else:
            return new_user


    def get_user_by_id(user_id: int):
        ...


    def get_user_by_email(email: EmailStr):
        ...
    
    def update_user(id: int):
        ...

    def delete_user(user_id: int):
        ...
    